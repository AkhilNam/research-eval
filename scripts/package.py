#!/usr/bin/env python3
"""Build portable archives from an explicit allowlist; never collect paper drafts."""

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parents[1]
SKILL_FILES = (
    "SKILL.md",
    "references/rubric.md",
    "references/report-format.md",
)


def write_archive(destination, entries):
    # Read and validate all inputs before replacing an existing release archive.
    payloads = [(name, source.read_bytes()) for name, source in entries]
    with ZipFile(destination, "w", compression=ZIP_DEFLATED) as archive:
        for name, content in payloads:
            info = ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, content)
    print(destination.relative_to(ROOT))


def main():
    output = ROOT / "dist"
    output.mkdir(exist_ok=True)
    skill = ROOT / "skills" / "review-paper"
    write_archive(
        output / "review-paper.zip",
        [(f"review-paper/{name}", skill / name) for name in SKILL_FILES],
    )
    plugin_files = [".claude-plugin/plugin.json", "README.md"] + [
        f"skills/review-paper/{name}" for name in SKILL_FILES
    ]
    write_archive(
        output / "research-eval-plugin.zip",
        [(f"research-eval/{name}", ROOT / name) for name in plugin_files],
    )


if __name__ == "__main__":
    main()
