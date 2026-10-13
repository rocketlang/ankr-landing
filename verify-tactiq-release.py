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

Changed 13 October 2026, for rc14. That release moved to a new reference layout
(format 2: one signed FIT configuration per slot, the devicetree measured into PCR 1).
This script knew the older layout only and broke on rc14 with exit 3, which is no
verdict. It now reads the layout from the file. The older path is untouched and rc11,
rc12 and rc13 report what they did before. For format 2 the digests are computed from
the payload bytes in u-boot.itb and in the FIT. A layout the script does not know is a
failed check. Not checked on that path: the signature on each FIT configuration.

Changed again 13 October 2026, the same day, after attacking the revision. THIS ONE
CHANGES WHAT EVERY RELEASE REPORTS. The script used to verify the signature over
SHA256SUMS against whatever certificate lay beside it. A release with a file altered,
its line rewritten and the sums re-signed with a home-made certificate passed: 13 of 13
on rc13. It now requires that the certificate was issued by Sigstore's CA to this
repository's release workflow, that the log entry is about this very signature, and that
the log's checkpoint and the entry's time are signed by the log's key. The CA
certificates and the log key are pinned in this script; see the note at the pins.
Complete releases now report: rc11 13, rc12 18, rc13 18, rc14 20 (before: 11, 13, 13).

One absence is still a note and not a failure: SHA256SUMS.sigstore.json, and since
13 October 2026 for rc11 only. rc11 never shipped one. Until that day the script could
not tell a release that never had a bundle from a later one whose bundle was left out,
so rc13 without its bundle passed with a shorter count. The release is now read from
the signing certificate, which the CA signed, and any tag but v2.1.0-rc11 must have its
bundle. That rc11 is the only such release is written into this script.

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
import tempfile

# ── PINNED: WHO MAY HAVE SIGNED, AND WHICH LOG ───────────────────────────────
#
# Until 13 October 2026 this script verified the signature over SHA256SUMS against the
# certificate that sits beside it, and asked nothing about that certificate. Found by
# attacking it that day: alter a file, rewrite its line in SHA256SUMS, sign the new
# SHA256SUMS with a certificate made on your own machine and dated to cover the day of
# the real log entry, and leave the real Sigstore bundle where it is. This script said
# "13 passed, 0 failed" on rc13, exit 0. It took its trust anchor from the thing it was
# verifying, the same fault the vendor found in the L3 checker on 28 September, and it
# had been here since the first version.
#
# What is pinned now, and where each value comes from:
#   the Fulcio root and intermediate: Sigstore's trusted_root.json
#     (github.com/sigstore/root-signing, targets/trusted_root.json, fetched 13 October
#     2026, sha256 6494e21e…e6bc0b66); DER sha256 3ba7b6cc…a54680c1 and 15d79534…087efe47
#   the Rekor log key: the same file; sha256 of its DER is the log ID c0d23d6a…9591801d.
#     The vendor ships the same key as rekor-sigstore.pub; it is not read from there
#   the identity: this repository's release-sign workflow, at a tag, with a token from
#     GitHub Actions
# WHAT THE PINS REST ON: one fetch from GitHub over TLS on one day. They show a
# certificate was issued by the CA Sigstore publishes; they do not make GitHub or
# Sigstore honest. Nothing is fetched at run time.
FULCIO_ROOT_PEM = """-----BEGIN CERTIFICATE-----
MIIB9zCCAXygAwIBAgIUALZNAPFdxHPwjeDloDwyYChAO/4wCgYIKoZIzj0EAwMw
KjEVMBMGA1UEChMMc2lnc3RvcmUuZGV2MREwDwYDVQQDEwhzaWdzdG9yZTAeFw0y
MTEwMDcxMzU2NTlaFw0zMTEwMDUxMzU2NThaMCoxFTATBgNVBAoTDHNpZ3N0b3Jl
LmRldjERMA8GA1UEAxMIc2lnc3RvcmUwdjAQBgcqhkjOPQIBBgUrgQQAIgNiAAT7
XeFT4rb3PQGwS4IajtLk3/OlnpgangaBclYpsYBr5i+4ynB07ceb3LP0OIOZdxex
X69c5iVuyJRQ+Hz05yi+UF3uBWAlHpiS5sh0+H2GHE7SXrk1EC5m1Tr19L9gg92j
YzBhMA4GA1UdDwEB/wQEAwIBBjAPBgNVHRMBAf8EBTADAQH/MB0GA1UdDgQWBBRY
wB5fkUWlZql6zJChkyLQKsXF+jAfBgNVHSMEGDAWgBRYwB5fkUWlZql6zJChkyLQ
KsXF+jAKBggqhkjOPQQDAwNpADBmAjEAj1nHeXZp+13NWBNa+EDsDP8G1WWg1tCM
WP/WHPqpaVo0jhsweNFZgSs0eE7wYI4qAjEA2WB9ot98sIkoF3vZYdd3/VtWB5b9
TNMea7Ix/stJ5TfcLLeABLE4BNJOsQ4vnBHJ
-----END CERTIFICATE-----
"""
FULCIO_INTERMEDIATE_PEM = """-----BEGIN CERTIFICATE-----
MIICGjCCAaGgAwIBAgIUALnViVfnU0brJasmRkHrn/UnfaQwCgYIKoZIzj0EAwMw
KjEVMBMGA1UEChMMc2lnc3RvcmUuZGV2MREwDwYDVQQDEwhzaWdzdG9yZTAeFw0y
MjA0MTMyMDA2MTVaFw0zMTEwMDUxMzU2NThaMDcxFTATBgNVBAoTDHNpZ3N0b3Jl
LmRldjEeMBwGA1UEAxMVc2lnc3RvcmUtaW50ZXJtZWRpYXRlMHYwEAYHKoZIzj0C
AQYFK4EEACIDYgAE8RVS/ysH+NOvuDZyPIZtilgUF9NlarYpAd9HP1vBBH1U5CV7
7LSS7s0ZiH4nE7Hv7ptS6LvvR/STk798LVgMzLlJ4HeIfF3tHSaexLcYpSASr1kS
0N/RgBJz/9jWCiXno3sweTAOBgNVHQ8BAf8EBAMCAQYwEwYDVR0lBAwwCgYIKwYB
BQUHAwMwEgYDVR0TAQH/BAgwBgEB/wIBADAdBgNVHQ4EFgQU39Ppz1YkEZb5qNjp
KFWixi4YZD8wHwYDVR0jBBgwFoAUWMAeX5FFpWapesyQoZMi0CrFxfowCgYIKoZI
zj0EAwMDZwAwZAIwPCsQK4DYiZYDPIaDi5HFKnfxXx6ASSVmERfsynYBiX2X6SJR
nZU84/9DZdnFvvxmAjBOt6QpBlc4J/0DxvkTCqpclvziL6BCCPnjdlIB3Pu3BxsP
mygUY7Ii2zbdCdliiow=
-----END CERTIFICATE-----
"""
REKOR_PUB_PEM = """-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE2G2Y+2tabdTV5BcGiBIx0a9fAFwr
kBbmLSGtks4L3qX6yYY0zufBnhC8Ur/iy55GhWP/9A/bY2LhC30M9+RYtw==
-----END PUBLIC KEY-----
"""
REKOR_LOG_ID = "c0d23d6ad406973f9559f3ba2d1ca01f84147d8ffc5b8445c224f98b9591801d"
SIGNER_SAN_PREFIX = ("URI:https://github.com/revenue7-eng/tactiq-os/.github/workflows/"
                     "release-sign.yml@refs/tags/")
SIGNER_TOKEN_ISSUER = "https://token.actions.githubusercontent.com"
# The one release that shipped no Sigstore bundle. For every other tag its absence fails.
NO_BUNDLE_TAGS = {"v2.1.0-rc11"}

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

    tag = check_signer(pem)

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
        if tag not in NO_BUNDLE_TAGS:
            bad("SHA256SUMS.sigstore.json is not present",
                f"every release after rc11 ships its log bundle (this one: {tag or 'tag unknown'}); "
                "without it nothing shows the signature was made while the certificate was valid")
        if expired:
            note("certificate has EXPIRED — `openssl dgst -verify` does not check this")
        if n_certs == 1:
            note("only the leaf certificate is present — the chain cannot be validated offline")
        note("no transparency-log entry or timestamp in the directory — nothing shows "
             "the signature was made while the certificate was valid")


def check_signer(pem):
    """
    Whose certificate is it? Added 13 October 2026; see the note at the pins above.
    A signature that verifies under a certificate says only that the holder of that
    certificate's key signed. These two checks say the certificate came from Sigstore's
    CA and was issued to this repository's release workflow.
    """
    with tempfile.TemporaryDirectory() as t:
        rootp, interp = os.path.join(t, "root.pem"), os.path.join(t, "inter.pem")
        open(rootp, "w").write(FULCIO_ROOT_PEM)
        open(interp, "w").write(FULCIO_INTERMEDIATE_PEM)
        # A Fulcio certificate lives ten minutes, so the chain is judged at a moment
        # inside the certificate's own window. When the signature was made is a
        # different question, answered from the log further down.
        nb = _cert_time(pem, "-startdate")
        if nb is None:
            bad("the signing certificate could not be read",
                "who signed SHA256SUMS is NOT established")
            return
        r = subprocess.run(["openssl", "verify", "-attime", str(int(nb.timestamp()) + 1),
                            "-purpose", "any", "-CAfile", rootp, "-untrusted", interp, pem],
                           capture_output=True, text=True)
    if r.returncode == 0:
        ok("the signing certificate was issued by Sigstore's CA (root and intermediate "
           "pinned in this script)")
    else:
        bad("the signing certificate was NOT issued by Sigstore's CA",
            "anyone can make a certificate and sign with it; the signature above then "
            "says nothing about who signed")
    san = subprocess.run(["openssl", "x509", "-in", pem, "-noout", "-ext", "subjectAltName"],
                         capture_output=True, text=True).stdout
    uris = [x.strip() for line in san.splitlines()[1:] for x in line.split(",") if x.strip()]
    txt = subprocess.run(["openssl", "x509", "-in", pem, "-noout", "-text"],
                         capture_output=True, text=True).stdout.split("\n")
    issuer = ""
    for i, l in enumerate(txt):
        if "1.3.6.1.4.1.57264.1.1:" in l and i + 1 < len(txt):
            issuer = txt[i + 1].strip()
    if len(uris) == 1 and uris[0].startswith(SIGNER_SAN_PREFIX) and issuer == SIGNER_TOKEN_ISSUER:
        ok("it was issued to this repository's release-sign workflow, at tag "
           + uris[0][len(SIGNER_SAN_PREFIX):])
        # the tag is believed only if the CA vouched for the certificate that states it
        return uris[0][len(SIGNER_SAN_PREFIX):] if r.returncode == 0 else None
    bad("the signing certificate was NOT issued to this repository's release workflow",
        f"identity: {', '.join(uris) or 'none'} · token issuer: {issuer or 'none'}")
    return None


def check_log_binding(d, e):
    """
    Is the log entry about THIS signature, and is it the real log's? Added 13 October
    2026. Until then the inclusion proof was recomputed and nothing tied it to the files:
    any genuine entry from any signing would have recomputed just as well.
    """
    try:
        spec = json.loads(base64.b64decode(e["canonicalizedBody"]))["spec"]
        want_hash = spec["data"]["hash"]["value"].lower()
        want_sig = base64.b64decode(spec["signature"]["content"])
        want_cert = base64.b64decode(spec["signature"]["publicKey"]["content"])
        der = lambda pem_bytes: subprocess.run(["openssl", "x509", "-outform", "DER"],
                                               input=pem_bytes, capture_output=True).stdout
        same = (hashlib.sha256(open(os.path.join(d, "SHA256SUMS"), "rb").read()).hexdigest() == want_hash
                and base64.b64decode(open(os.path.join(d, "SHA256SUMS.workflow.sig"), "rb").read()) == want_sig
                and der(want_cert) and der(want_cert) == der(open(os.path.join(d, "SHA256SUMS.workflow.pem"), "rb").read()))
    except Exception:
        same = False
    if same:
        ok("the log entry is about this SHA256SUMS, this signature and this certificate")
    else:
        bad("the log entry is NOT about this SHA256SUMS, signature and certificate",
            "an entry for some other signing proves nothing about this one")

    with tempfile.TemporaryDirectory() as t:
        key = os.path.join(t, "rekor.pem")
        open(key, "w").write(REKOR_PUB_PEM)

        def signed_by_log(msg, sig):
            mp, sp = os.path.join(t, "m"), os.path.join(t, "s")
            open(mp, "wb").write(msg); open(sp, "wb").write(sig)
            return subprocess.run(["openssl", "dgst", "-sha256", "-verify", key, "-signature", sp, mp],
                                  capture_output=True).returncode == 0

        good = False
        try:
            log_id = base64.b64decode(e["logId"]["keyId"]).hex()
            ip = e["inclusionProof"]
            body, _, sigs = ip["checkpoint"]["envelope"].partition("\n\n")
            lines = body.split("\n")
            raw = b""
            for l in sigs.splitlines():
                parts = l.split(" ")
                if len(parts) == 3 and parts[1] == "rekor.sigstore.dev":
                    raw = base64.b64decode(parts[2])
            good = (log_id == REKOR_LOG_ID and raw[:4].hex() == REKOR_LOG_ID[:8]
                    and lines[1] == str(ip["treeSize"]) and lines[2] == ip["rootHash"]
                    and signed_by_log((body + "\n").encode(), raw[4:]))
        except Exception:
            good = False
        if good:
            ok("the log's checkpoint is signed by Rekor's key (pinned in this script) and "
               "states the tree the proof leads to")
        else:
            bad("the log's checkpoint is NOT signed by Rekor's key, or states another tree",
                "the inclusion proof then leads to a root nobody vouches for")

        good = False
        try:
            payload = json.dumps({"body": e["canonicalizedBody"], "integratedTime": int(e["integratedTime"]),
                                  "logID": REKOR_LOG_ID, "logIndex": int(e["logIndex"])},
                                 sort_keys=True, separators=(",", ":")).encode()
            good = signed_by_log(payload, base64.b64decode(e["inclusionPromise"]["signedEntryTimestamp"]))
        except Exception:
            good = False
        if good:
            ok("the time of the entry is signed by Rekor's key")
        else:
            bad("the time of the entry is NOT signed by Rekor's key",
                "the comparison with the certificate's window below rests on an unsigned time")


def check_transparency(d, cert_expired):
    """
    The Rekor inclusion proof, verified OFFLINE. Returns True when a bundle was found.

    This answers the one question an expired signing certificate leaves open: was the
    signature made while that certificate was live? The log entry carries a timestamp,
    and the inclusion proof shows the entry is in a tree with a given root — both
    checkable here with no network call, which is the whole claim being tested.

    Until 13 October 2026 the checkpoint signature was not checked, and this text said
    so: the root was recomputed and compared with the root the bundle states, which shows
    the entry is consistent with that root and not that the root is the real log's. Since
    that day check_log_binding verifies the checkpoint and the entry's time under Rekor's
    key, pinned in this script, and ties the entry to the files. Still not checked:
    whether the log shows this entry today. Nothing is fetched.
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

    check_log_binding(d, e)

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

    note("the checkpoint is a statement the log signed once; whether the log still shows "
         "this entry today is not checked here, since nothing is fetched")
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

    # Which reference is this? Until 13 October 2026 this script knew one layout and
    # broke on any other (rc14: KeyError, exit 3, no verdict). The layout is now read
    # from the file, and one this script does not know is a FAILED check, not a crash.
    fmt = ref.get("format")
    if fmt == "tactiq-pcr-reference/2" and ref.get("boot_path") == "bootm":
        check_reference_bootm(d, ref)
        return
    if "kernel_sha256" not in C or "cmdline" not in C or "fdt_sha256" not in C:
        bad(f"the PCR reference is in a layout this script does not know (format: {fmt}, "
            f"boot path: {ref.get('boot_path')})",
            "the boot measurements were NOT recomputed")
        return

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


def fit_payloads(buf):
    """Image name -> payload bytes, whether the FIT keeps data inline or after the tree."""
    total = struct.unpack_from(">I", buf, 4)[0]
    base = (total + 3) & ~3
    root = parse_fdt(buf)["nodes"][""]
    out = {}
    for nm, n in root["nodes"]["images"]["nodes"].items():
        p = n["props"]
        if "data" in p:
            out[nm] = p["data"]
        elif "data-size" in p and ("data-position" in p or "data-offset" in p):
            size = int.from_bytes(p["data-size"], "big")
            off = (int.from_bytes(p["data-position"], "big") if "data-position" in p
                   else base + int.from_bytes(p["data-offset"], "big"))
            if off + size <= len(buf):
                out[nm] = buf[off:off + size]
    return root, out


def check_reference_bootm(d, ref):
    """
    The format-2 reference, new in rc14 (added 13 October 2026). The loader runs bootm
    with one signed FIT configuration per slot. The kernel command line sits in /chosen
    of that configuration's devicetree, and U-Boot 2026.10 measures the devicetree into
    PCR 1, so PCR 1 has one value per slot and PCR 0 no longer takes the devicetree.

    Recipe read from the header of the vendor's mk-pcr-reference.py; that script is not
    run. Unlike the older path above, every digest used here is computed from the
    payload bytes in u-boot.itb and in the FIT, not read from a hash node or from the
    reference's own components block.

    NOT CHECKED HERE: the signature on each FIT configuration (only that one is there),
    and the reference's statements about the loader's compiled-in environment.
    """
    C = ref["components"]
    need = {"u-boot-rock5a.itb": None, "fitImage-rock5a": None}
    for f in need:
        fp = os.path.join(d, f)
        if not os.path.exists(fp):
            bad(f"{f} not present", "the boot measurements were NOT recomputed")
            return
        need[f] = open(fp, "rb").read()
    itb, fit = need["u-boot-rock5a.itb"], need["fitImage-rock5a"]

    try:
        _, uimgs = fit_payloads(itb)
        froot, fimgs = fit_payloads(fit)
    except Exception as e:
        bad("could not parse u-boot.itb or the FIT image", f"{type(e).__name__}: {e} — "
            "the boot measurements were NOT recomputed")
        return
    spl, agree = [], 0
    for m in C["spl_measurements"]:
        data = uimgs.get(m["image"])
        if data is None:
            bad(f"u-boot.itb holds no payload for {m['image']}")
            continue
        h = sha(data)
        spl.append((m["pcr"], h))
        if h.hex() == m["sha256"]:
            agree += 1
        else:
            bad(f"the payload of {m['image']} in u-boot.itb does not hash to the reference")
    if agree == len(C["spl_measurements"]) and agree:
        ok(f"{agree} loader payload(s) hashed from u-boot.itb agree with the reference")

    ver = C["uboot_version"].encode()
    if ver in itb:
        ok("the loader version string the reference names is in u-boot.itb")
    else:
        note("the loader version string was not found as plain bytes in u-boot.itb; "
             "PCR 0 below still rests on it")

    confs = froot["nodes"].get("configurations", {}).get("nodes", {})
    slot_fdt, slot_kernel = {}, {}
    for slot, s in sorted(C["slots"].items()):
        c = confs.get(s["fit_configuration"])
        if c is None:
            bad(f"slot {slot}: the FIT has no configuration {s['fit_configuration']}")
            continue
        kn = c["props"].get("kernel", b"").rstrip(b"\0").decode()
        fn = c["props"].get("fdt", b"").rstrip(b"\0").decode()
        if kn not in fimgs or fn not in fimgs:
            bad(f"slot {slot}: the configuration's kernel or devicetree payload is not in the FIT")
            continue
        kh, fh = sha(fimgs[kn]), sha(fimgs[fn])
        good = True
        if kh.hex() != s["kernel_sha256"]:
            bad(f"slot {slot}: the kernel payload in the FIT does not hash to the reference"); good = False
        if fh.hex() != s["fdt_sha256"]:
            bad(f"slot {slot}: the devicetree payload in the FIT does not hash to the reference"); good = False
        try:
            chosen = parse_fdt(fimgs[fn])["nodes"][""]["nodes"]["chosen"]["props"]
            ba = chosen.get("bootargs", b"").rstrip(b"\0").decode()
        except Exception:
            ba = ""
        if not ba or ba != s["cmdline"]:
            bad(f"slot {slot}: /chosen bootargs in the slot's devicetree is not the command "
                "line the reference gives"); good = False
        if not any(k.startswith("signature") for k in c["nodes"]):
            bad(f"slot {slot}: the FIT configuration carries no signature node"); good = False
        if good:
            slot_kernel[slot], slot_fdt[slot] = kh, fh
            ok(f"slot {slot}: kernel, devicetree and command line read from the FIT agree "
               "with the reference (the configuration's signature is NOT verified here)")
    if sorted(slot_fdt) != sorted(C["slots"]) or not slot_fdt:
        bad("not every slot could be read from the FIT", "the PCR values were NOT recomputed")
        return
    if len(set(slot_kernel.values())) != 1:
        bad("the slots boot different kernels; the reference gives one PCR 8")
        return

    def value(ds):
        v = ZERO
        for x in ds:
            v = ext(v, x)
        return v

    crtm = sha(ver + b"\0")
    chain = {i: [] for i in range(10)}
    chain[0].append(crtm)
    for p, h in spl:
        chain[p].append(h)
    chain[0].append(crtm)
    chain[8].append(next(iter(slot_kernel.values())))
    chain[9].append(sha(b"initrd\0"))
    agree = total = 0
    for i in range(10):
        if i == 1:
            for slot, fh in sorted(slot_fdt.items()):
                total += 1
                got = value([fh, sha(C.get("bootargs", "").encode() + b"\0"), SEP]).hex()
                want = str(ref["pcr"]["1"].get(slot, "")).lower()
                if got == want:
                    agree += 1
                else:
                    bad(f"PCR1[{slot}] does not recompute", f"published {want}\n        computed  {got}")
            continue
        total += 1
        got = value(chain[i] + ([SEP] if i < 8 else [])).hex()
        want = str(ref["pcr"][str(i)]).lower()
        if got == want:
            agree += 1
        else:
            bad(f"PCR{i} does not recompute", f"published {want}\n        computed  {got}")
    if agree == total:
        ok(f"{agree} PCR value(s) recompute from a second implementation (PCR 1 once per slot)")


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
