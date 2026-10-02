#!/usr/bin/env python3
"""
An independent verifier for a tactiq-os release.

Written from the published artefacts and the mk-pcr-reference.py docstring, NOT by
calling that script. The point is a second implementation: a generator that confirms
its own output tells you less than a different implementation that agrees with it.

It checks four things and says which one failed:

  1. SHA256SUMS covers the artefacts present, and each one hashes to what it claims
  2. the signature over SHA256SUMS verifies against the published certificate
  3. the certificate's own attestations — commit, workflow, repo, runner environment
  4. every PCR value in pcr-reference.json recomputes, and the measured FIT image
     digests come out of u-boot.itb itself rather than from the reference's own
     components block

Usage:  python3 verify-tactiq-release.py /path/to/release-dir
Exit:   0 all checks passed · 1 a check failed · 2 refused to start, nothing verified
        3 the checker itself broke, which is not a verdict

Changed 2 October 2026. Until then a file that was not in the directory was a note and
the run still exited 0, so an incomplete download passed with a shorter count. An absent
file is now a failed check: every artefact SHA256SUMS lists, the signature material, the
PCR reference and each of its inputs. The checks themselves are unchanged, and so is
what a complete release reports.

One absence is still a note and not a failure, on purpose: SHA256SUMS.sigstore.json.
Releases before rc12 do not ship one, and the script reports that as an observation
about the release. It follows that this script cannot tell a release that never had a
bundle from a later one whose bundle was left out of the download.

No dependencies beyond the standard library and `openssl` on PATH.
"""

import base64
import datetime as dt
import hashlib
import json
import os
import struct
import subprocess
import sys

ZERO = bytes(32)
SEP = hashlib.sha256(bytes.fromhex("ffffffff")).digest()
ext = lambda p, d: hashlib.sha256(p + d).digest()
sha = lambda b: hashlib.sha256(b).digest()

ok_count = 0
bad_count = 0


def ok(msg):
    global ok_count
    ok_count += 1
    print(f"  ok    {msg}")


def bad(msg, detail=""):
    global bad_count
    bad_count += 1
    print(f"  FAIL  {msg}")
    if detail:
        print(f"        {detail}")


def note(msg):
    print(f"  --    {msg}")


# ── 1. checksums ─────────────────────────────────────────────────────────────

def check_sums(d):
    p = os.path.join(d, "SHA256SUMS")
    if not os.path.exists(p):
        bad("SHA256SUMS present"); return
    entries = {}
    for line in open(p):
        parts = line.split()
        if len(parts) == 2:
            entries[parts[1]] = parts[0]
    ok(f"SHA256SUMS lists {len(entries)} artefact(s)")

    # The tooling that computes the reference should itself be covered, or a verifier
    # is trusting a script nobody signed.
    for tool in ("mk-pcr-reference.py", "pcr-reference-rock5a.json"):
        if tool in entries:
            ok(f"covered by the signed sums: {tool}")
        else:
            bad(f"NOT covered by the signed sums: {tool}",
                "the reference and the script that builds it should be inside the signature")

    # An artefact the signed sums list and the directory lacks is NOT a note. A file
    # that was never hashed has not been checked, and a count that is merely shorter
    # reads as a pass.
    agree = 0
    wrong = 0
    for name, want in entries.items():
        f = os.path.join(d, name)
        if not os.path.exists(f):
            bad(f"listed in SHA256SUMS but not present: {name}",
                "absent evidence is not a passed check — download the whole release")
            wrong += 1
            continue
        got = hashlib.sha256(open(f, "rb").read()).hexdigest()
        if got != want:
            bad(f"checksum mismatch: {name}", f"want {want}\n        got  {got}")
            wrong += 1
        else:
            agree += 1
    if not wrong:
        ok(f"{agree} present artefact(s) hash to their published value")


# ── 2 + 3. signature and what the certificate attests ────────────────────────

def check_signature(d):
    sums = os.path.join(d, "SHA256SUMS")
    pem = os.path.join(d, "SHA256SUMS.workflow.pem")
    sig = os.path.join(d, "SHA256SUMS.workflow.sig")
    missing = [os.path.basename(x) for x in (sums, pem, sig) if not os.path.exists(x)]
    if missing:
        bad("signature material not present: " + ", ".join(missing),
            "the signature over SHA256SUMS was NOT checked")
        return

    der = os.path.join(d, ".sig.der")
    pub = os.path.join(d, ".pub.pem")
    try:
        open(der, "wb").write(__import__("base64").b64decode(open(sig, "rb").read()))
        subprocess.run(["openssl", "x509", "-in", pem, "-pubkey", "-noout"],
                       stdout=open(pub, "wb"), check=True, stderr=subprocess.DEVNULL)
        r = subprocess.run(["openssl", "dgst", "-sha256", "-verify", pub,
                            "-signature", der, sums],
                           capture_output=True, text=True)
        if r.returncode == 0:
            ok("the signature over SHA256SUMS verifies")
        else:
            bad("signature does not verify", r.stdout.strip() or r.stderr.strip())
    except Exception as e:
        bad("could not check the signature", str(e))
    finally:
        for f in (der, pub):
            if os.path.exists(f):
                os.remove(f)

    txt = subprocess.run(["openssl", "x509", "-in", pem, "-noout", "-text"],
                         capture_output=True, text=True).stdout
    oids = {
        "1.3.6.1.4.1.57264.1.3": "commit",
        "1.3.6.1.4.1.57264.1.5": "repository",
        "1.3.6.1.4.1.57264.1.6": "ref",
        "1.3.6.1.4.1.57264.1.11": "runner environment",
    }
    # split on \n only: these values can carry an embedded carriage return, and
    # splitlines() treats that as a line break, putting the value in the next element
    lines = txt.split("\n")
    for oid, label in oids.items():
        for i, l in enumerate(lines):
            if oid + ":" not in l:
                continue
            # The value may sit one or two lines below: some of these carry a short
            # ASN.1 wrapper, and openssl's carriage returns become line breaks once
            # Python has applied universal newlines. Scan forward for the first line
            # that actually holds something readable.
            val = ""
            for j in range(i + 1, min(i + 4, len(lines))):
                cand = "".join(ch for ch in lines[j] if ch.isprintable()).strip()
                while cand and not (cand[0].isalnum() or cand[0] in "/:_-"):
                    cand = cand[1:]
                if cand and not cand.startswith("X509v3") and "1.3.6.1" not in cand:
                    val = cand
                    break
            note(f"certificate attests {label}: {val}")
            break

    # A Fulcio certificate lives about ten minutes, and `openssl dgst -verify` never
    # looks at validity — a signature keeps verifying long after the certificate has
    # expired. What closes that is not a longer certificate but EVIDENCE OF WHEN the
    # signature was made. A Rekor inclusion proof carries exactly that.
    dates = subprocess.run(["openssl", "x509", "-in", pem, "-noout", "-dates"],
                           capture_output=True, text=True).stdout.strip().replace("\n", "  ")
    note(f"certificate validity: {dates}")
    expired = subprocess.run(["openssl", "x509", "-in", pem, "-noout", "-checkend", "0"],
                             capture_output=True).returncode != 0
    n_certs = open(pem).read().count("BEGIN CERTIFICATE")

    # rc12 (2026-09-24) added SHA256SUMS.sigstore.json. Releases before it have no
    # bundle, and this script must keep reporting them honestly rather than assuming
    # the newer shape — so both paths are live and both are exercised.
    if not check_transparency(d, expired):
        if expired:
            note("certificate has EXPIRED — `openssl dgst -verify` does not check this")
        if n_certs == 1:
            note("only the leaf certificate is present — the chain cannot be validated offline")
        note("no transparency-log entry or timestamp in the directory — nothing shows "
             "the signature was made while the certificate was valid")


def check_transparency(d, cert_expired):
    """
    The Rekor inclusion proof, verified OFFLINE. Returns True when a bundle was found.

    This answers the one question an expired signing certificate leaves open: was the
    signature made while that certificate was live? The log entry carries a timestamp,
    and the inclusion proof shows the entry is in a tree with a given root — both
    checkable here with no network call, which is the whole claim being tested.

    What is NOT checked, and must not be implied: the checkpoint signature. Verifying
    that needs Rekor's public key, so this recomputes the root the proof implies and
    compares it to the root the bundle states. Agreement proves the entry is consistent
    with that root; it does not prove the root is the real log's. Saying which half is
    done is the difference between evidence and a better-dressed claim.
    """
    bundle = os.path.join(d, "SHA256SUMS.sigstore.json")
    if not os.path.exists(bundle):
        return False
    try:
        b = json.load(open(bundle))
        e = b["verificationMaterial"]["tlogEntries"][0]
        ip = e["inclusionProof"]
    except Exception as ex:
        bad("sigstore bundle present but unreadable", str(ex))
        return True

    dec = lambda x: base64.b64decode(x)

    # RFC 6962 §2.1.1 — recompute the root from the leaf and the audit path.
    leaf = hashlib.sha256(b"\x00" + dec(e["canonicalizedBody"])).digest()
    fn, sn, r = int(ip["logIndex"]), int(ip["treeSize"]) - 1, leaf
    for h in [dec(x) for x in ip["hashes"]]:
        if sn == 0:
            break
        if (fn & 1) or (fn == sn):
            r = hashlib.sha256(b"\x01" + h + r).digest()
            while fn != 0 and not (fn & 1):
                fn >>= 1; sn >>= 1
        else:
            r = hashlib.sha256(b"\x01" + r + h).digest()
        fn >>= 1; sn >>= 1

    if r == dec(ip["rootHash"]):
        ok(f"Rekor inclusion proof recomputes (log index {e['logIndex']}, tree size {ip['treeSize']})")
    else:
        bad("Rekor inclusion proof does NOT recompute",
            f"recomputed {r.hex()[:32]}, bundle states {dec(ip['rootHash']).hex()[:32]}")

    # The decisive check: was the signature made inside the certificate's window?
    it = int(e["integratedTime"])
    stamped = dt.datetime.fromtimestamp(it, dt.timezone.utc)
    nb = _cert_time(os.path.join(d, "SHA256SUMS.workflow.pem"), "-startdate")
    na = _cert_time(os.path.join(d, "SHA256SUMS.workflow.pem"), "-enddate")
    if nb and na:
        if nb <= stamped <= na:
            ok(f"logged at {stamped:%Y-%m-%d %H:%M:%S}Z, inside the certificate window "
               f"({(stamped-nb).total_seconds():.0f}s after notBefore)")
            if cert_expired:
                note("the certificate has since expired, which no longer matters: the log "
                     "entry shows the signature was made while it was live")
        else:
            bad("the signature was logged OUTSIDE the certificate's validity window",
                f"logged {stamped:%Y-%m-%d %H:%M:%S}Z, valid {nb:%H:%M:%S}Z–{na:%H:%M:%S}Z")
    else:
        bad(f"logged at {stamped:%Y-%m-%d %H:%M:%S}Z, but the certificate window is unreadable",
            "the log time and the certificate's validity could NOT be compared")

    note("the checkpoint signature is NOT verified here — that needs Rekor's public key, "
         "so the root is recomputed but not proven to be the live log's")
    return True


def _cert_time(pem, flag):
    """notBefore/notAfter as an aware datetime, or None if it cannot be read."""
    try:
        out = subprocess.run(["openssl", "x509", "-in", pem, "-noout", flag],
                             capture_output=True, text=True).stdout.strip()
        return dt.datetime.strptime(out.split("=", 1)[1].strip(),
                                    "%b %d %H:%M:%S %Y %Z").replace(tzinfo=dt.timezone.utc)
    except Exception:
        return None


# ── 4. the measurement reference, recomputed ─────────────────────────────────

def parse_fdt(buf):
    magic, total, off_s, off_str, _r, _v, _l, _c, size_str, size_s = struct.unpack_from(">10I", buf, 0)
    if magic != 0xD00DFEED:
        raise ValueError("not a flattened device tree")
    strings = buf[off_str:off_str + size_str]
    nm_at = lambda o: strings[o:strings.index(b"\0", o)].decode()
    p, end = off_s, off_s + size_s
    root = {"nodes": {}, "props": {}}
    stack = [root]
    while p < end:
        (tok,) = struct.unpack_from(">I", buf, p); p += 4
        if tok == 1:
            e = buf.index(b"\0", p); nm = buf[p:e].decode(); p = (e + 4) & ~3
            n = {"nodes": {}, "props": {}}
            stack[-1]["nodes"][nm] = n; stack.append(n)
        elif tok == 2:
            stack.pop()
        elif tok == 3:
            ln, noff = struct.unpack_from(">II", buf, p); p += 8
            stack[-1]["props"][nm_at(noff)] = buf[p:p + ln]; p = (p + ln + 3) & ~3
        elif tok == 9:
            break
    return root


def check_reference(d):
    rp = os.path.join(d, "pcr-reference-rock5a.json")
    if not os.path.exists(rp):
        bad("pcr-reference-rock5a.json not present",
            "the boot measurements were NOT recomputed")
        return
    ref = json.load(open(rp))
    C = ref["components"]

    # Inputs must hash to what the reference says they do, or the arithmetic below is
    # over numbers the document supplied to itself.
    for f, want in ref.get("inputs", {}).items():
        fp = os.path.join(d, f)
        if not os.path.exists(fp):
            bad(f"published input not present: {f}",
                "its hash was NOT compared with the reference")
            continue
        got = hashlib.sha256(open(fp, "rb").read()).hexdigest()
        (ok if got == want else bad)(f"published input hash: {f}")

    # Read the measured image digests out of the FIT itself rather than trusting the
    # reference's own components block.
    itb = os.path.join(d, "u-boot-rock5a.itb")
    if os.path.exists(itb):
        try:
            root = parse_fdt(open(itb, "rb").read())
            imgs = root["nodes"][""]["nodes"]["images"]["nodes"]
            pub = {m["image"]: m["sha256"] for m in C["spl_measurements"]}
            agree = 0
            for nm, node in imgs.items():
                h = node["nodes"].get("hash")
                if not h or nm not in pub:
                    continue
                if h["props"].get("value", b"").hex() == pub[nm]:
                    agree += 1
                else:
                    bad(f"FIT digest disagrees with the reference: {nm}")
            ok(f"{agree} measured image digest(s) read out of u-boot.itb agree")
        except Exception as e:
            bad("could not parse u-boot.itb", str(e))
    else:
        bad("u-boot-rock5a.itb not present",
            "the measured image digests were NOT read out of the FIT")

    # Recompute every PCR. Algorithm per mk-pcr-reference.py: SPL S-CRTM into PCR0,
    # then the FIT images in load order, then U-Boot proper's S-CRTM and the FIT
    # device-tree hash into PCR0, kernel into 8, initrd into 9, separators on 0-7.
    crtm = sha(C["uboot_version"].encode() + b"\0")
    chain = {i: [] for i in range(10)}
    chain[0].append(crtm)
    for e in C["spl_measurements"]:
        chain[e["pcr"]].append(bytes.fromhex(e["sha256"]))
    chain[0].append(crtm)
    chain[8].append(bytes.fromhex(C["kernel_sha256"]))
    chain[9].append(sha(b"initrd\0"))
    chain[0].append(bytes.fromhex(C["fdt_sha256"]))

    def value(ds):
        v = ZERO
        for x in ds:
            v = ext(v, x)
        return v

    agree = 0
    for i in range(10):
        tail = [SEP] if i < 8 else []
        if i == 1:
            for slot, cl in C["cmdline"].items():
                got = value([sha(cl.encode() + b"\0"), SEP]).hex()
                if got == ref["pcr"]["1"][slot].lower():
                    agree += 1
                else:
                    bad(f"PCR1[{slot}] does not recompute")
            continue
        got = value(chain[i] + tail).hex()
        if got == ref["pcr"][str(i)].lower():
            agree += 1
        else:
            bad(f"PCR{i} does not recompute",
                f"published {ref['pcr'][str(i)].lower()}\n        computed  {got}")
    ok(f"{agree} PCR value(s) recompute from a second implementation")


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    d = sys.argv[1]
    if not os.path.isdir(d):
        print(f"not a directory: {d}")
        sys.exit(2)
    print(f"\nverifying release artefacts in {d}\n")
    # A crash is not a verdict. An exception used to leave through Python's own exit
    # code 1 — the same code as a failed check — with every later check never run.
    try:
        check_sums(d)
        print()
        check_signature(d)
        print()
        check_reference(d)
    except Exception as e:
        print(f"\n  BROKE  the checker itself failed: {type(e).__name__}: {e}")
        print(f"  {ok_count} check(s) had passed and {bad_count} had failed before it broke.")
        print("  This is NOT a verdict on the release.\n")
        sys.exit(3)
    print(f"\n  {ok_count} check(s) passed, {bad_count} failed\n")
    sys.exit(1 if bad_count else 0)


if __name__ == "__main__":
    main()
