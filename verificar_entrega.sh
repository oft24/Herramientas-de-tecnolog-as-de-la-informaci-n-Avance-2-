#!/bin/bash
set -u
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR" || exit 1

TOTAL=0
OK=0
check() {
  TOTAL=$((TOTAL+1))
  if eval "$2"; then
    echo "  [OK] $1"
    OK=$((OK+1))
  else
    echo "  [ ] $1"
  fi
}

echo "=================================================="
echo " Verificacion de entrega - Avance 2 del Reto"
echo "=================================================="
check "Hay codigo de aplicacion en app/" "[ -n \"\$(find app -type f ! -name '.gitkeep' 2>/dev/null)\" ]"
check "Existe docker-compose.yml" "[ -f docker-compose.yml ]"
SERVICIOS=$(awk '/^services:/ {dentro=1; next} /^[a-zA-Z_-]+:/ {dentro=0} dentro && /^  [a-zA-Z0-9_-]+:/ {n++} END {print n+0}' docker-compose.yml 2>/dev/null)
check "Compose define al menos 2 servicios (encontrados: $SERVICIOS)" "[ \"$SERVICIOS\" -ge 2 ]"
check "Existe Dockerfile endurecido" "grep -q 'HEALTHCHECK' Dockerfile && grep -q '^USER appuser' Dockerfile"
check "Existe endpoint /salud" "grep -rq '/salud' app/"
check "Existe IaC de S3 y RDS" "grep -rqi 's3' infra/ && grep -rqi 'db_instance\|rds' infra/"
check "Hay pipeline propio" "[ -n \"\$(find pipeline -type f ! -name '.gitkeep' 2>/dev/null)\" ]"
check "Existe evidencia roja" "[ -s reportes/corrida_roja.txt ] && grep -qi 'BLOQUEADO' reportes/corrida_roja.txt"
check "Existe evidencia verde" "[ -s reportes/corrida_verde.txt ] && grep -qi 'PERMITIDO' reportes/corrida_verde.txt"
check "Existe SBOM CycloneDX" "[ -s reportes/sbom_cyclonedx.json ] && grep -q 'CycloneDX' reportes/sbom_cyclonedx.json"
check "Documentacion principal completa" "[ -f docs/README.md ] && [ -f docs/ADR-001-decisiones-tecnicas.md ] && [ -f docs/tabla_decisiones_pipeline.md ] && [ -f docs/declaracion_uso_ia.md ]"
check "Hay diagrama de arquitectura" "[ -n \"\$(find docs -iname 'diagrama*' 2>/dev/null)\" ]"
check "No hay marcadores [COMPLETAR]" "! grep -Rqi '\[COMPLETAR\]' docs/ 2>/dev/null"
check "No se sube .env" "[ ! -f .env ] && grep -q '^\.env$' .gitignore"
check "Existe video o enlace real" "[ -n \"\$(find video -type f ! -name '.gitkeep' 2>/dev/null)\" ] || { [ -f docs/enlace_video.txt ] && ! grep -qi 'todavía no está grabado' docs/enlace_video.txt; }"
echo "=================================================="
echo " Resultado: $OK / $TOTAL"
echo "=================================================="
[ "$OK" -eq "$TOTAL" ]
