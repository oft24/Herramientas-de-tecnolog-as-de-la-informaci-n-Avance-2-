"""Security and quality gate with one integrated final decision."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def stage(name: str, checks: list[str]) -> bool:
    print(f"\n[ETAPA] {name}")
    if checks:
        for check in checks:
            print(f"  [HALLAZGO] {check}")
        print(f"  [BLOQUEA] {name}: umbral incumplido")
        return False
    print("  [OK] Sin hallazgos sobre el umbral definido")
    return True


def tracked_files() -> list[Path]:
    files = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or ".venv" in path.parts:
            continue
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif", ".woff", ".woff2"}:
            continue
        files.append(path)
    return files


def secret_scan(root: Path) -> list[str]:
    findings = []
    assignment = re.compile(r"(?:AWS_SECRET_ACCESS_KEY|AWS_ACCESS_KEY_ID|DB_PASSWORD|FLASK_SECRET_KEY)\s*=\s*[^\s#]+", re.I)
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
            continue
        if any(part in {".git", ".venv", "venv", "node_modules", "__pycache__"} for part in path.parts):
            continue
        if path.name == ".env":
            # Local development configuration is intentionally ignored by Git.
            # A tracked .env is still caught by the repository hygiene check.
            if path.is_relative_to(ROOT):
                tracked = subprocess.run(
                    ["git", "ls-files", "--error-unmatch", str(path.relative_to(ROOT))],
                    cwd=ROOT,
                    capture_output=True,
                )
                if tracked.returncode:
                    continue
        if path.name in {"run_pipeline.py", "generate_sbom.py"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for line_number, line in enumerate(text.splitlines(), 1):
            if ".example" in path.name and "replace-with" in line:
                continue
            if assignment.search(line):
                label = path.relative_to(ROOT) if path.is_relative_to(ROOT) else path.name
                findings.append(f"{label}:{line_number}: asignación de secreto")
            if "BEGIN PRIVATE KEY" in line:
                label = path.relative_to(ROOT) if path.is_relative_to(ROOT) else path.name
                findings.append(f"{label}:{line_number}: llave privada")
    return findings


def iac_scan() -> list[str]:
    text = (ROOT / "infra" / "main.tf").read_text(encoding="utf-8")
    required = {
        "bloqueo de acceso público S3": "aws_s3_bucket_public_access_block",
        "cifrado S3": "sse_algorithm = \"AES256\"",
        "cifrado RDS": "storage_encrypted       = true",
        "RDS privado": "publicly_accessible     = false",
    }
    return [f"{label}: falta '{needle}'" for label, needle in required.items() if needle not in text]


def docker_scan() -> list[str]:
    text = (ROOT / "Dockerfile").read_text(encoding="utf-8")
    checks = {
        "imagen base versionada": re.search(r"^FROM\s+\S+:\S+", text, re.M),
        "usuario no root": re.search(r"^USER\s+appuser", text, re.M),
        "healthcheck": re.search(r"^HEALTHCHECK\s+", text, re.M),
    }
    return [f"Dockerfile: falta {label}" for label, found in checks.items() if not found]


def tests() -> list[str]:
    compile_result = subprocess.run(
        [sys.executable, "-m", "compileall", "-q", "app"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if compile_result.returncode:
        return [compile_result.stdout or compile_result.stderr or "compileall falló"]
    environment = {**os.environ, "PYTHONPATH": str(ROOT / "app")}
    unit_result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "app/tests", "-p", "test_app.py"],
        cwd=ROOT,
        env=environment,
        capture_output=True,
        text=True,
    )
    if unit_result.returncode:
        return [unit_result.stdout[-1200:] or unit_result.stderr[-1200:] or "pruebas unitarias fallaron"]
    return []


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo-red", action="store_true", help="agrega un archivo temporal con un secreto para demostrar el bloqueo")
    args = parser.parse_args()
    print("PIPELINE DANGOKO AVANCE 2")
    print("Umbral integrado: cero hallazgos HIGH/CRITICAL y pruebas de sintaxis correctas")
    checks: list[bool] = []
    checks.append(stage("Pruebas de sintaxis", tests()))
    with tempfile.TemporaryDirectory(prefix="dangoko-pipeline-") as temp_dir:
        scan_root = ROOT
        if args.demo_red:
            fixture = Path(temp_dir) / "malicious.env"
            fixture.write_text("AWS_SECRET_ACCESS_KEY=demo-secret-that-must-block\n", encoding="utf-8")
            scan_root = Path(temp_dir)
            print(f"Demo roja: se inspecciona un candidato real en {fixture.name}")
        checks.append(stage("Higiene de secretos", secret_scan(scan_root)))
    checks.append(stage("Infraestructura como código", iac_scan()))
    checks.append(stage("Docker endurecido", docker_scan()))
    subprocess.run([sys.executable, str(ROOT / "pipeline" / "generate_sbom.py")], cwd=ROOT, check=True)
    checks.append(stage("SBOM CycloneDX", []))
    if all(checks):
        print("\nDECISIÓN FINAL: PERMITIDO")
        return 0
    print("\nDECISIÓN FINAL: BLOQUEADO")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
