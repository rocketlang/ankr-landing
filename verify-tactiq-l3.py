#!/usr/bin/env python3
"""
An independent checker for the TactiQ OS rc13 L3 evidence.

Written from the artefacts and the wire formats, NOT by running VERIFY-L3-rc13.md's
commands. tpm2-tools is not installed here, so the quote signature and the attestation
structure are parsed and verified in Python from the TPM specification rather than by
tpm2_checkquote. That is the point: a second implementation that agrees tells you more
than the vendor's own tool agreeing with itself.

It checks, and says which failed:

  1. the archive's own SHA256SUMS covers the files present and each one hashes
  2. the EK certificate chains to the pinned Infineon root through the intermediate
  3. the registration record's CMS signature verifies, and its signer chains to the
     signing CA
  4. the AK name in the record equals 000b || sha256(public area) of the ak.pub supplied
  5. each quote is a genuine TPMS_ATTEST: TPM_GENERATED magic, type ATTEST_QUOTE
  6. each quote's signature verifies under the AK public key (ECDSA P-256 / SHA-256),
     implemented here, not delegated
  7. each quote's extraData equals sha256 of its own .msg — the anti-replay binding
  8. the quote's pcrDigest equals sha256 of PCR 0..9 concatenated from the signed RIM
  9. the RIM's own CMS signature verifies against the release root

WHAT IT CANNOT DO, and nobody should read past this. Credential activation binds the AK
to the EK, and it is unreplayable by a third party by construction: it needs the TPM's
private EK. So the AK-to-TPM link here rests on the registrar's signed statement, which
the vendor discloses himself. This script verifies that the statement is properly signed.
It does not, and cannot, verify that the statement is true.

Usage:  python3 verify-tactiq-l3.py /path/to/rc13-dir
Exit:   0 all checks passed · 1 something did not · 2 could not run the check
"""

import hashlib
import json
import os
import subprocess
import sys

# ── PINNED TRUST ANCHORS ─────────────────────────────────────────────────────
#
# These do not come from the archive, and that is the entire point.
#
# An earlier version of this script trusted signing-ca.pem and infineon-root.crt
# out of the evidence archive itself, with openssl's -partial_chain, which says
# "treat this supplied CA as a trust anchor". The archive's own SHA256SUMS is not
# signed. The vendor demonstrated the consequence on 2026-09-28: change a field in
# the registration record, sign it under a CA of your own, replace the three files,
# recompute the archive sums — and this script reported 15 passed, 0 failed on a
# set it should have rejected outright.
#
# A verifier that takes its trust anchors from the thing it is verifying is not a
# verifier. The anchor must be pinned here or supplied from outside the archive.

# The Infineon OPTIGA(TM) RSA Root CA, by fingerprint of its DER encoding.
#
# PROVENANCE: this value was first observed in the rc13 evidence set, which on its own
# would only detect a CHANGED root and not one forged before anyone looked. On
# 2026-09-29 it was compared against the copy Infineon itself publishes:
#
#     https://pki.infineon.com/OptigaRsaRootCA/OptigaRsaRootCA.crt
#     1455 bytes DER, TLS chain verified, CN = Infineon OPTIGA(TM) RSA Root CA,
#     serial 03, valid 2013-07-26 to 2043-07-25 — BYTE-IDENTICAL to the archived copy.
#
# What that establishes: the root in the evidence archive is the one the manufacturer
# publishes today, so the pin no longer rests on the vendor's own bundle alone.
# What it does NOT establish: that Infineon's endpoint was not itself compromised, and
# the comparison was made in 2026, not in 2013. Independent, not absolute.
#
# The check below stays OFFLINE by design — the fingerprint is hard-coded, nothing is
# fetched at run time. Re-confirm the URL by hand if this script is ever revised.
INFINEON_ROOT_SHA256 = "899e35474c9807eb4c7f2f7a12da0028fb250cd02154d0009fca7d9c66574f3b"

# The role-specific EKU the Registration Signer must carry. `-purpose any` does not
# look at extended key usage at all, so without this check any leaf chaining to the
# release root would do — including one issued for an entirely different role.
REG_SIGNER_EKU_OID = "2.25.205994972697553183157730487844756597568"

# @rule:required-evidence-is-required
#
# Every file below is needed by a check. An earlier version NOTED its absence and
# skipped the check, so deleting evidence produced a clean run with a lower count:
# remove ak.pub and both quote signatures go unverified, remove the .p7s and the
# registration signature is never checked — 0 failures either way. An attacker does
# not have to forge what they can simply delete.
#
# Missing required evidence is a FAILURE, not a note. Found 2026-09-29 by deleting
# files one at a time and watching the script stay green.
REQUIRED = [
    "registration-TACTIQ-BENCH-001.json",
    "registration-TACTIQ-BENCH-001.json.p7s",
    "reg-signer.pem", "signing-ca.pem",
    "ek.der", "infineon-mfr034.crt", "infineon-root.crt",
    "ak.pub", "SHA256SUMS",
]

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


def sh(*args):
    return subprocess.run(args, capture_output=True, text=True)


# ── 1. the archive's own sums ────────────────────────────────────────────────

def check_archive_sums(e):
    f = os.path.join(e, "SHA256SUMS")
    if not os.path.exists(f):
        note("no SHA256SUMS inside the evidence archive")
        return
    n = miss = 0
    for line in open(f):
        line = line.strip()
        if not line or " " not in line:
            continue
        want, name = line.split(None, 1)
        name = name.lstrip("*").strip()
        p = os.path.join(e, name)
        if not os.path.exists(p):
            miss += 1
            continue
        got = hashlib.sha256(open(p, "rb").read()).hexdigest()
        if got != want:
            bad(f"archive sum mismatch: {name}", f"want {want[:16]}… got {got[:16]}…")
            return
        n += 1
    ok(f"{n} file(s) in the archive hash to the archive's own SHA256SUMS")
    if miss:
        note(f"{miss} listed file(s) absent from the archive")


# ── 2 + 3. the certificate chains ────────────────────────────────────────────

def check_chains(e):
    ek, inter, root = (os.path.join(e, x) for x in
                       ("ek.der", "infineon-mfr034.crt", "infineon-root.crt"))

    # The root shipped in the archive is checked against the PINNED fingerprint
    # before it is used for anything. Without this, an attacker who replaces the
    # root also replaces what it is compared to.
    if os.path.exists(root):
        got = hashlib.sha256(subprocess.run(["openssl", "x509", "-in", root, "-outform", "DER"],
                                            capture_output=True).stdout).hexdigest()
        if got == INFINEON_ROOT_SHA256:
            ok("the Infineon root in the archive matches the pinned fingerprint")
            note("the pin itself was corroborated 2026-09-29 against the copy Infineon "
                 "publishes at pki.infineon.com — byte-identical")
        else:
            bad("the Infineon root in the archive is NOT the pinned root",
                f"pinned {INFINEON_ROOT_SHA256[:24]}… archive {got[:24]}…")
            return

    if all(os.path.exists(x) for x in (ek, inter, root)):
        r = sh("openssl", "verify", "-partial_chain", "-trusted", root,
               "-untrusted", inter, "-inform", "DER", ek)
        # openssl wants PEM for -inform on verify in some builds; convert and retry
        if r.returncode != 0:
            pem = os.path.join(e, "_ek.pem")
            sh("openssl", "x509", "-inform", "DER", "-in", ek, "-out", pem)
            r = sh("openssl", "verify", "-partial_chain", "-trusted", root,
                   "-untrusted", inter, pem)
        if r.returncode == 0:
            ok("EK certificate chains to the pinned Infineon root via the intermediate")
        else:
            bad("EK certificate does NOT chain to the pinned root",
                (r.stdout + r.stderr).strip().splitlines()[-1] if (r.stdout + r.stderr).strip() else "")
    else:
        bad("EK or Infineon chain files absent — the TPM is UNVERIFIED")

    signer, ca = os.path.join(e, "reg-signer.pem"), os.path.join(e, "signing-ca.pem")
    if os.path.exists(signer) and os.path.exists(ca):
        r = sh("openssl", "verify", "-partial_chain", "-trusted", ca, signer)
        if r.returncode == 0:
            ok("registration signer chains to the signing CA")
        else:
            bad("registration signer does NOT chain to the signing CA",
                (r.stdout + r.stderr).strip())
    else:
        bad("registration signer or signing CA absent — signer chain UNVERIFIED")


def check_registration_sig(e, root):
    """
    The record's signature, anchored OUTSIDE the archive. @rule:trust-the-anchor

    signing-ca.pem is passed as an UNTRUSTED INTERMEDIATE (-certfile), never as a
    trust anchor (-CAfile with -partial_chain). The distinction is the whole check:
    with -partial_chain a re-signed set carrying its own CA verifies happily, which
    is exactly the forgery the vendor demonstrated. Anchored at the release root,
    the same forged set is rejected because its CA chains to nothing we trust.
    """
    rec = os.path.join(e, "registration-TACTIQ-BENCH-001.json")
    p7s = rec + ".p7s"
    inter = os.path.join(e, "signing-ca.pem")
    if not all(os.path.exists(x) for x in (rec, p7s)):
        bad("registration record or its signature is absent",
            "this is required evidence; its absence is a failure, not a skip")
        return
    if not root:
        bad("no release root supplied — the record cannot be anchored",
            "put release-root-r2.pem beside the release assets; the archive's own CA is not a trust anchor")
        return

    args = ["openssl", "cms", "-verify", "-binary", "-inform", "DER", "-in", p7s,
            "-content", rec, "-CAfile", root, "-purpose", "any", "-out", os.devnull]
    if os.path.exists(inter):
        args += ["-certfile", inter]
    r = sh(*args)
    if r.returncode == 0:
        ok("the registration record's signature chains to the RELEASE ROOT (not the archive's CA)")
    else:
        bad("the registration record does NOT chain to the release root",
            (r.stderr or r.stdout).strip().splitlines()[-1] if (r.stderr or r.stdout).strip() else "")
        return

    # -purpose any ignores extended key usage entirely, so without this any leaf
    # chaining to the release root would pass — including one issued for another role.
    signer = os.path.join(e, "reg-signer.pem")
    if os.path.exists(signer):
        # Prove the signature came from THAT certificate, not merely from some valid leaf
        # under the same root. Without this the EKU is read off a file on disk while the
        # CMS could have been signed by a different leaf entirely — the RIM Signer, say —
        # and every check would still pass. The vendor's own VERIFY-L3 does this and this
        # script did not; adopted from his procedure 2026-09-29.
        cap = os.path.join(e, "_cms-signer.pem")
        sh("openssl", "cms", "-verify", "-binary", "-inform", "DER", "-in", p7s,
           "-content", rec, "-CAfile", root, "-certfile", inter, "-purpose", "any",
           "-signer", cap, "-out", os.devnull)
        if os.path.exists(cap):
            fa = sh("openssl", "x509", "-in", cap, "-noout", "-fingerprint", "-sha256").stdout.strip()
            fb = sh("openssl", "x509", "-in", signer, "-noout", "-fingerprint", "-sha256").stdout.strip()
            try: os.unlink(cap)
            except OSError: pass
            if fa and fa == fb:
                ok("the CMS was signed by the Registration Signer in the archive, not merely by a valid leaf")
            else:
                bad("the record was signed by a DIFFERENT certificate than reg-signer.pem",
                    "a valid leaf under the same root is not the Registration Signer")
        eku = sh("openssl", "x509", "-in", signer, "-noout", "-ext", "extendedKeyUsage").stdout
        if REG_SIGNER_EKU_OID in eku:
            ok("the Registration Signer carries its role-specific extended key usage")
        else:
            bad("the Registration Signer does NOT carry the expected EKU",
                f"expected {REG_SIGNER_EKU_OID}, cert says: {' '.join(eku.split())[:80]}")
        chain = sh("openssl", "verify", "-CAfile", root, "-untrusted", inter, signer)
        if chain.returncode == 0:
            ok("the Registration Signer chains to the release root")
        else:
            bad("the Registration Signer does NOT chain to the release root",
                (chain.stdout + chain.stderr).strip().splitlines()[-1])


# ── 4. the AK is the one the record names ────────────────────────────────────

def check_ak_name(e):
    akp, rec = os.path.join(e, "ak.pub"), os.path.join(e, "registration-TACTIQ-BENCH-001.json")
    if not (os.path.exists(akp) and os.path.exists(rec)):
        bad("ak.pub or the registration record is absent",
            "without the AK the quotes cannot be attributed to a registered key")
        return None
    raw = open(akp, "rb").read()
    # TPM2B_PUBLIC: 2-byte size, then the public area the name is computed over.
    area = raw[2:]
    name = "000b" + hashlib.sha256(area).hexdigest()
    claimed = json.load(open(rec)).get("ak_name", "").lower()
    if name == claimed:
        ok(f"AK name matches the record (000b…{name[-12:]})")
    else:
        bad("the AK supplied is NOT the AK the record registers",
            f"computed {name[:24]}… record {claimed[:24]}…")
    # ek.der and the intermediate are in the archive and covered only by its UNSIGNED
    # sums. The signed record carries both in hex, so compare them: otherwise a
    # different genuine Infineon TPM's certificate can be substituted unnoticed.
    rj = json.load(open(rec))
    for fn, field in (("ek.der", "ek_certificate"), ("infineon-mfr034.crt", "intermediate_certificate")):
        fp = os.path.join(e, fn)
        if not os.path.exists(fp) or field not in rj:
            continue
        raw = open(fp, "rb").read()
        if not raw.startswith(b"\x30"):                       # PEM on disk → DER
            raw = subprocess.run(["openssl", "x509", "-in", fp, "-outform", "DER"],
                                 capture_output=True).stdout
        if raw.hex().lower() == str(rj[field]).lower():
            ok(f"{fn} matches the certificate named in the signed record")
        else:
            bad(f"{fn} does NOT match the signed record",
                "a substituted certificate — the record names a different one")

    return area


# ── 5-8. the quotes ──────────────────────────────────────────────────────────

TPM_GENERATED = 0xFF544347
ST_ATTEST_QUOTE = 0x8018


def parse_attest(b):
    """TPMS_ATTEST → dict. Only the fields this check needs."""
    o = 0
    magic = int.from_bytes(b[o:o + 4], "big"); o += 4
    typ = int.from_bytes(b[o:o + 2], "big"); o += 2
    n = int.from_bytes(b[o:o + 2], "big"); o += 2 + n            # qualifiedSigner
    n = int.from_bytes(b[o:o + 2], "big"); o += 2
    extra = b[o:o + n]; o += n                                    # extraData
    o += 17                                                       # clockInfo
    o += 8                                                        # firmwareVersion
    # TPMS_QUOTE_INFO: TPML_PCR_SELECTION then TPM2B_DIGEST
    cnt = int.from_bytes(b[o:o + 4], "big"); o += 4
    sel = []
    for _ in range(cnt):
        o += 2                                                    # hash alg
        sz = b[o]; o += 1
        sel.append(b[o:o + sz].hex()); o += sz
    n = int.from_bytes(b[o:o + 2], "big"); o += 2
    return {"magic": magic, "type": typ, "extra": extra,
            "pcr_select": sel, "pcr_digest": b[o:o + n].hex()}


def ak_pubkey(area):
    """The P-256 public key out of a TPMT_PUBLIC ECC area."""
    from cryptography.hazmat.primitives.asymmetric import ec
    # type(2) nameAlg(2) attrs(4) authPolicy(2B) symmetric(2) scheme(2) schemeHash(2)
    # curve(2) kdf(2) then TPMS_ECC_POINT: x(2B) y(2B)
    o = 2 + 2 + 4
    o += 2 + int.from_bytes(area[o:o + 2], "big")                 # authPolicy
    o += 2 + 2 + 2 + 2 + 2                                        # parms
    xl = int.from_bytes(area[o:o + 2], "big"); o += 2
    x = area[o:o + xl]; o += xl
    yl = int.from_bytes(area[o:o + 2], "big"); o += 2
    y = area[o:o + yl]
    return ec.EllipticCurvePublicNumbers(
        int.from_bytes(x, "big"), int.from_bytes(y, "big"), ec.SECP256R1()).public_key()


def check_quotes(e, area, rim_digest):
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.exceptions import InvalidSignature

    ids = sorted({f.rsplit(".", 1)[0] for f in os.listdir(e) if f.endswith(".attest")})
    if not ids:
        note("no .attest files — no quotes to check")
        return
    key = ak_pubkey(area) if area else None

    for q in ids:
        att = open(os.path.join(e, q + ".attest"), "rb").read()
        a = parse_attest(att)

        if a["magic"] == TPM_GENERATED and a["type"] == ST_ATTEST_QUOTE:
            ok(f"{q}: genuine TPMS_ATTEST, type ATTEST_QUOTE (pcrSelect {','.join(a['pcr_select'])})")
        else:
            bad(f"{q}: not a TPM quote structure",
                f"magic {a['magic']:#x} type {a['type']:#x}")
            continue

        sig_p = os.path.join(e, q + ".sig")
        if key and os.path.exists(sig_p):
            sig = open(sig_p, "rb").read()
            try:
                key.verify(sig, att, ec.ECDSA(hashes.SHA256()))
                ok(f"{q}: quote signature verifies under the registered AK")
            except InvalidSignature:
                bad(f"{q}: quote signature does NOT verify under the registered AK")
        else:
            bad(f"{q}: signature or AK absent — the quote is UNVERIFIED")

        msg_p = os.path.join(e, q + ".msg")
        if os.path.exists(msg_p):
            want = hashlib.sha256(open(msg_p, "rb").read()).digest()
            if a["extra"] == want:
                ok(f"{q}: extraData binds this quote to its own .msg")
            else:
                bad(f"{q}: extraData does NOT match sha256 of its .msg",
                    f"quote {a['extra'].hex()[:24]}… msg {want.hex()[:24]}…")
        else:
            bad(f"{q}: no .msg — the anti-replay binding cannot be checked")

        if rim_digest:
            hit = [sl for sl, dg in rim_digest.items() if dg == a["pcr_digest"]]
            if hit:
                ok(f"{q}: attested boot state MATCHES the signed reference (slot {hit[0]})")
            else:
                bad(f"{q}: attested boot state matches NEITHER boot slot in the reference",
                    f"quote {a['pcr_digest'][:24]}… slots " +
                    ", ".join(f"{sl}={dg[:12]}…" for sl, dg in rim_digest.items()))


# ── 9. the reference the quote is compared against ───────────────────────────

def rim_expected_all(d):
    """Both boot slots. Hardcoding slot A would report a genuine slot-B boot as drift."""
    out = {}
    for slot in ("A", "B"):
        dg = rim_expected(d, slot, quiet=True)
        if dg:
            out[slot] = dg
    if out:
        ok(f"reference boot state recomputed from the signed RIM for slot(s) {', '.join(out)}")
    return out


def rim_expected(d, slot="A", quiet=False):
    rim = os.path.join(d, "rim-rock5a.json")
    if not os.path.exists(rim):
        note("no rim-rock5a.json — nothing to compare the attested state against")
        return None
    v = json.load(open(rim))["pcr"]["values"]
    blob = b""
    for i in range(10):
        x = v[str(i)]
        h = x[slot] if isinstance(x, dict) else (x[0] if isinstance(x, list) else x)
        blob += bytes.fromhex(h)
    return hashlib.sha256(blob).hexdigest()


def check_rim_sig(d, e, root):
    rim, p7s = os.path.join(d, "rim-rock5a.json"), os.path.join(d, "rim-rock5a.json.p7s")
    if not (os.path.exists(rim) and os.path.exists(p7s)):
        note("RIM or its signature absent — not checked")
        return
    if not root:
        bad("no release root supplied — the RIM cannot be anchored",
            "release-root-r2.pem is a published RELEASE asset; it is not in the evidence archive")
        return
    r = sh("openssl", "cms", "-verify", "-binary", "-inform", "DER", "-in", p7s,
           "-content", rim, "-CAfile", root, "-purpose", "any", "-out", os.devnull)
    if r.returncode == 0:
        ok("the RIM's signature chains to the release root")
    else:
        bad("the RIM does NOT chain to the release root",
            (r.stderr or r.stdout).strip().splitlines()[-1] if (r.stderr or r.stdout).strip() else "")


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    d = sys.argv[1]
    e = os.path.join(d, "l3", "l3-evidence-rc13")
    if not os.path.isdir(e):
        for root, dirs, _ in os.walk(d):
            if "l3-evidence-rc13" in dirs:
                e = os.path.join(root, "l3-evidence-rc13")
                break
    if not os.path.isdir(e):
        print(f"no l3-evidence-rc13 directory under {d}", file=sys.stderr)
        return 2

    print("\n  the evidence archive\n")

    missing = [f for f in REQUIRED if not os.path.exists(os.path.join(e, f))]
    if missing:
        bad(f"{len(missing)} required file(s) missing from the evidence archive",
            ", ".join(missing) + " — absent evidence is not a passed check")
    else:
        ok(f"all {len(REQUIRED)} required evidence files are present")

    # every .attest needs its .sig and .msg, or the quote is unverifiable
    for q in sorted({f.rsplit(".", 1)[0] for f in os.listdir(e) if f.endswith(".attest")}):
        for ext in (".sig", ".msg"):
            if not os.path.exists(os.path.join(e, q + ext)):
                bad(f"{q}: {ext} is missing — the quote cannot be verified",
                    "a quote without its signature proves nothing")

    check_archive_sums(e)

    # The release root is a published RELEASE asset and must come from OUTSIDE the
    # evidence archive. Looked for beside the release assets, or given explicitly.
    root = os.environ.get("TACTIQ_RELEASE_ROOT")
    if not root or not os.path.exists(root):
        cand = os.path.join(d, "release-root-r2.pem")
        root = cand if os.path.exists(cand) else None
    if root and os.path.commonpath([os.path.abspath(root), os.path.abspath(e)]) == os.path.abspath(e):
        bad("the release root was found INSIDE the evidence archive — refusing to use it",
            "an anchor that travels with the thing it anchors is not an anchor")
        root = None
    if root:
        note(f"release root: {os.path.relpath(root, d)} (outside the archive)")
        # WHERE THE TRUST NOW SITS. Moving the anchor out of the archive fixed the
        # forgery, but it relocated the trust rather than removing it: this root is
        # NOT listed in the Sigstore-signed SHA256SUMS, so nothing independent binds
        # it. The vendor's own procedure says to confirm its fingerprint through a
        # second channel. This script cannot do that for you — it prints the value so
        # you can. A check you have to perform yourself is still a check; a check
        # nobody names is not.
        rd = subprocess.run(["openssl", "x509", "-in", root, "-outform", "DER"],
                            capture_output=True).stdout
        if rd:
            note(f"release root sha256: {hashlib.sha256(rd).hexdigest()}")

            # The vendor corrected an earlier, broader claim of ours (2026-09-29) and the
            # correction is verified here rather than taken on his word. The root is not
            # listed in SHA256SUMS directly — but the SIGNED RIM carries its SPKI hash at
            # keys.release_root.spki_sha256, and the RIM itself IS in the signed sums.
            # So a root swapped on the release page AFTER the tag was signed is caught.
            # That turns what we published as an open limit into an actual check.
            spki = subprocess.run(["openssl", "x509", "-in", root, "-pubkey", "-noout"],
                                  capture_output=True).stdout
            der = subprocess.run(["openssl", "pkey", "-pubin", "-outform", "DER"],
                                 input=spki, capture_output=True).stdout
            spki_sha = hashlib.sha256(der).hexdigest() if der else None
            rim_path = os.path.join(d, "rim-rock5a.json")

            # CIRCULARITY GUARD. The RIM names the release root, and the RIM's own CMS
            # signature chains TO that root — so on its own the pair proves nothing: an
            # attacker who forges a root and re-signs the RIM satisfies both. Found by
            # attacking this file on 2026-09-29, after adding the spki check.
            #
            # The property the vendor actually described is a Sigstore one: the RIM is
            # listed in the RELEASE SHA256SUMS, and that file is signed by the workflow
            # with a Rekor inclusion proof. So the RIM's bytes must be pinned to the
            # release sums BEFORE anything it says is used. Without this the spki check
            # is decoration.
            rim_pinned = False
            rel_sums = os.path.join(d, "SHA256SUMS")
            if os.path.exists(rim_path) and os.path.exists(rel_sums):
                want = None
                for line in open(rel_sums):
                    parts = line.split()
                    if len(parts) == 2 and parts[1] == "rim-rock5a.json":
                        want = parts[0].lower()
                got = hashlib.sha256(open(rim_path, "rb").read()).hexdigest()
                if want is None:
                    bad("rim-rock5a.json is not listed in the release SHA256SUMS",
                        "nothing signed binds the RIM, so what it names cannot be trusted")
                elif want != got:
                    bad("rim-rock5a.json does NOT match the release SHA256SUMS",
                        f"sums say {want[:24]}… file is {got[:24]}…")
                else:
                    ok("the RIM is pinned to the release SHA256SUMS (Sigstore-signed; "
                       "the release checker verifies that signature)")
                    rim_pinned = True
            else:
                bad("cannot pin the RIM to the release SHA256SUMS",
                    "rim-rock5a.json or the release SHA256SUMS is absent")

            declared = None
            if rim_pinned:
                try:
                    declared = json.load(open(rim_path)).get("keys", {}).get("release_root", {}).get("spki_sha256")
                except Exception:
                    declared = None
            if declared and spki_sha:
                if declared == spki_sha:
                    ok("the release root is bound INSIDE the signed RIM (spki_sha256 matches)")
                else:
                    bad("the release root does NOT match the one named in the signed RIM",
                        f"RIM says {declared[:24]}… root is {spki_sha[:24]}…")
            else:
                # Absent is a FAILED check, never a skipped one.
                bad("the signed RIM does not name a release_root spki_sha256",
                    "cannot confirm the root against the signed set")

            note("WHAT REMAINS: the workflow and the release page are ONE channel, so this "
                 "catches a post-signing swap, not whoever controls the repository from the "
                 "start. Confirm the fingerprint elsewhere for that.")
    else:
        note("no release-root-r2.pem found beside the release assets — anchored checks will FAIL")

    print("\n  the chains of trust\n")
    check_chains(e)
    check_registration_sig(e, root)

    print("\n  the attestation key\n")
    area = check_ak_name(e)

    print("\n  the reference\n")
    check_rim_sig(d, e, root)
    rim_digest = rim_expected_all(d)

    print("\n  the quotes\n")
    check_quotes(e, area, rim_digest)

    print("\n  what this cannot establish\n")
    note("credential activation binds the AK to the EK and is unreplayable by a third")
    note("party by construction — it needs the TPM's private EK. The AK-to-TPM link")
    note("therefore rests on the registrar's signed statement, verified above as")
    note("properly signed. That the statement is TRUE is not checked and cannot be.")

    rec = os.path.join(e, "registration-TACTIQ-BENCH-001.json")
    if os.path.exists(rec):
        r = json.load(open(rec))
        for k in ("revocation_checked", "signed"):
            if k in r and r[k] is False:
                note(f"the record itself declares {k} = false")

    print(f"\n  {ok_count} check(s) passed, {bad_count} failed\n")
    return 0 if bad_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
