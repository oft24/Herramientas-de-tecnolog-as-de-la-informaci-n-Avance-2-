"""Generate a small CycloneDX SBOM from the pinned Python requirements."""

from __future__ import annotations

import json
import re
from pathlib import Path
from datetime import datetime, timezone


ROOT = Path(__file__).resolve().parents[1]
REQUIREMENTS = ROOT / "app" / "requirements.txt"
OUTPUT = ROOT / "reportes" / "sbom_cyclonedx.json"


def components() -> list[dict]:
    result = []
    for line in REQUIREMENTS.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        match = re.match(r"([A-Za-z0-9_.-]+)(?:\[[^]]+\])?==([A-Za-z0-9_.+-]+)", line)
        if not match:
            continue
        name, version = match.groups()
        result.append({
            "type": "library",
            "bom-ref": f"pkg:pypi/{name.lower()}@{version}",
            "name": name,
            "version": version,
            "purl": f"pkg:pypi/{name.lower()}@{version}",
            "scope": "required",
        })
    return result


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    document = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.5",
        "serialNumber": "urn:uuid:2c1d1f77-9ef3-4b04-82cc-8d1d6db0fb52",
        "version": 1,
        "metadata": {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tools": [{"vendor": "dangoko", "name": "pipeline/generate_sbom.py", "version": "1.0.0"}],
        },
        "components": components(),
    }
    OUTPUT.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"SBOM CycloneDX generado: {OUTPUT.relative_to(ROOT)} ({len(document['components'])} componentes)")


if __name__ == "__main__":
    main()
