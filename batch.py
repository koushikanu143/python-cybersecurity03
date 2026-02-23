import argparse
import hashlib
import os
import subprocess
from pathlib import Path
from typing import Iterable, List, Tuple


PE_EXTS = {".exe", ".dll", ".sys", ".scr", ".cpl", ".drv"}  # optional extras


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def find_pe_files(root: Path, recursive: bool = True) -> Iterable[Path]:
    if recursive:
        for p in root.rglob("*"):
            if p.is_file() and p.suffix.lower() in PE_EXTS:
                yield p
    else:
        for p in root.glob("*"):
            if p.is_file() and p.suffix.lower() in PE_EXTS:
                yield p


def run_pestudiox(pestudiox: Path, input_file: Path, output_xml: Path, timeout: int) -> Tuple[int, str]:
    """
    Runs: pestudiox -file:<input> -xml:<output>
    Returns (returncode, stderr_text).
    """
    # PEStudio expects the -file: and -xml: style arguments (no space after colon).
    cmd = [
        str(pestudiox),
        f"-file:{str(input_file)}",
        f"-xml:{str(output_xml)}",
    ]

    p = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout,
        shell=False,
    )
    return p.returncode, (p.stderr or "").strip()


def main() -> None:
    ap = argparse.ArgumentParser(description="Batch analyze PE files using PEStudio CLI (pestudiox.exe).")
    ap.add_argument("--pestudiox", required=True, help=r"Full path to pestudiox.exe (e.g. C:\Tools\pestudio\pestudiox.exe)")
    ap.add_argument("--input", required=True, help=r"Folder containing .exe files (e.g. C:\Samples)")
    ap.add_argument("--output", required=True, help=r"Folder to write XML reports (e.g. C:\Reports)")
    ap.add_argument("--no-recursive", action="store_true", help="Do not scan subfolders")
    ap.add_argument("--timeout", type=int, default=120, help="Timeout per file (seconds)")
    args = ap.parse_args()

    pestudiox = Path(args.pestudiox).expanduser().resolve()
    in_dir = Path(args.input).expanduser().resolve()
    out_dir = Path(args.output).expanduser().resolve()
    recursive = not args.no_recursive

    if not pestudiox.exists():
        raise FileNotFoundError(f"pestudiox.exe not found: {pestudiox}")
    if not in_dir.exists() or not in_dir.is_dir():
        raise NotADirectoryError(f"Input folder not found / not a folder: {in_dir}")

    out_dir.mkdir(parents=True, exist_ok=True)

    files: List[Path] = list(find_pe_files(in_dir, recursive=recursive))
    if not files:
        print(f"No PE files found in {in_dir} (extensions: {sorted(PE_EXTS)})")
        return

    print(f"Found {len(files)} file(s). Writing reports to: {out_dir}")

    ok = 0
    failed = 0

    for i, f in enumerate(files, start=1):
        try:
            h = sha256_file(f)
            # Name output by hash to avoid collisions
            xml_path = out_dir / f"{f.stem}_{h[:12]}.xml"

            rc, err = run_pestudiox(pestudiox, f, xml_path, timeout=args.timeout)

            if rc == 0 and xml_path.exists() and xml_path.stat().st_size > 0:
                ok += 1
                print(f"[{i}/{len(files)}] OK  -> {f}  =>  {xml_path.name}")
            else:
                failed += 1
                print(f"[{i}/{len(files)}] FAIL(rc={rc}) -> {f}")
                if err:
                    print(f"           stderr: {err}")

        except subprocess.TimeoutExpired:
            failed += 1
            print(f"[{i}/{len(files)}] TIMEOUT -> {f}")
        except Exception as e:
            failed += 1
            print(f"[{i}/{len(files)}] ERROR -> {f} ({e})")

    print("\nDone.")
    print(f"Success: {ok}")
    print(f"Failed : {failed}")


if __name__ == "__main__":
    main()