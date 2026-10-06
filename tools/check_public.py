"""Scan staged public blobs or every commit in a push range without opening private files."""

import argparse
import re
import shutil
import subprocess
from pathlib import PurePosixPath

PATTERNS = (
    re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(rb"(?:ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})"),
    re.compile(rb"AKIA[A-Z0-9]{16}"),
    re.compile(rb"/Users/[A-Za-z0-9_.-]+/|/home/[A-Za-z0-9_.-]+/"),
    re.compile(rb"(?:CLOUDFLARED_TOKEN|TUNNEL_TOKEN)[\"']?\s*[:=]\s*[\"']?[A-Za-z0-9+/=_-]{40,}"),
)
GIT = shutil.which("git")


def git(*args: str) -> bytes:
    if GIT is None:
        raise SystemExit("Public scan requires Git on PATH.")
    try:
        # Fixed read-only subcommands and argv data; never invoke a shell.
        result = subprocess.run(  # noqa: S603
            [GIT, *args], capture_output=True, check=False, timeout=30
        )
    except subprocess.TimeoutExpired:
        raise SystemExit(
            "Public scan timed out reading Git; check the repository and retry."
        ) from None
    if result.returncode:
        raise SystemExit("Public scan could not read Git objects; check the revision or index.")
    return result.stdout


def unsafe_path(path: str, mode: str) -> bool:
    parts = PurePosixPath(path).parts
    name = parts[-1].lower()
    return (
        mode == "120000"
        or name.endswith((".pdf", ".pem", ".key", ".p12", ".pfx", ".env"))
        or (name.startswith(".env") and name != ".env.example")
        or name.startswith(("secrets.", ".secrets.", "credentials.", ".credentials.", ".private."))
        or any(
            part.lower()
            in {
                "private",
                ".private",
                "private-notes",
                "secrets",
                ".secrets",
                "credentials",
                ".credentials",
            }
            for part in parts
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "revision_range", nargs="?", help="Scan BASE..HEAD, or all ancestors of HEAD"
    )
    parser.add_argument("--staged", action="store_true", help="Scan the complete staged tree")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        canaries = [
            b"-----BEGIN " + b"PRIVATE KEY-----",
            b"ghp_" + b"A" * 36,
            b"AKIA" + b"A" * 16,
            b"/Users/" + b"synthetic/private/",
            b"TUNNEL_TOKEN=" + b"synthetic" * 8,
        ]
        checks = [
            bool(pattern.search(value)) for pattern, value in zip(PATTERNS, canaries, strict=True)
        ]
        checks.extend(
            (
                unsafe_path("private/example.txt", "100644"),
                unsafe_path("example.PDF", "100644"),
                unsafe_path("portfolio.env", "100644"),
                unsafe_path("credentials.json", "100644"),
                not unsafe_path(".env.example", "100644"),
            )
        )
        if not all(checks):
            raise SystemExit("Public scan self-test failed; do not publish.")
        print("public-scan self-test: passed (synthetic canaries only)")
        return
    if args.staged == bool(args.revision_range):
        parser.error("choose either --staged or a revision range")
    if args.revision_range and (
        args.revision_range.startswith("-")
        or not re.fullmatch(r"[A-Za-z0-9_./~^+-]+", args.revision_range)
    ):
        parser.error("use a revision or range such as HEAD or origin/main..HEAD")
    revisions = (
        [None]
        if args.staged
        else git("rev-list", "--reverse", args.revision_range).decode().splitlines()
    )
    scanned, findings = 0, 0
    for revision in revisions:
        tree = (
            git("ls-files", "--stage", "-z")
            if revision is None
            else git("ls-tree", "-r", "-z", revision)
        )
        for record in tree.split(b"\0"):
            if not record:
                continue
            metadata, path = record.split(b"\t", 1)
            fields = metadata.decode().split()
            mode, object_id = fields[0], fields[1 if revision is None else 2]
            if mode == "160000":
                findings += 1
                continue
            if unsafe_path(path.decode(), mode):
                findings += 1
                continue
            blob = git("cat-file", "blob", object_id)
            findings += sum(bool(pattern.search(blob)) for pattern in PATTERNS)
            scanned += 1
    print(f"public-scan: {len(revisions)} trees, {scanned} blobs, {findings} findings")
    if not revisions or findings:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
