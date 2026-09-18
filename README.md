# Dangoko Marketplace — Avance 2

Aplicación de marketplace para productos asiáticos. El proyecto usa Flask, PostgreSQL, S3, Docker Compose y un servicio independiente de notificaciones. El flujo principal es: catálogo → carrito → pedido persistido en RDS → recibo privado en S3 → notificación.

La documentación académica está en [docs/README.md](docs/README.md). La aplicación vive en `app/`, la infraestructura como código en `infra/` y los controles del pipeline en `pipeline/`.

## Clonar el proyecto

```bash
git clone https://github.com/oft24/Herramientas-de-tecnolog-as-de-la-informaci-n-Avance-2-.git
cd Herramientas-de-tecnolog-as-de-la-informaci-n-Avance-2-
```

## Ejecutar localmente con Docker

Nunca copies credenciales reales al repositorio. Crea el archivo local desde la plantilla y completa sus valores únicamente en tu máquina o en la EC2:

```bash
cp .env.example .env
chmod 600 .env
docker compose up --build -d
curl http://127.0.0.1:5000/salud
docker compose ps
```

En PowerShell:

```powershell
Copy-Item .env.example .env
docker compose up --build -d
Invoke-WebRequest http://127.0.0.1:5000/salud
docker compose ps
```

## Variables mínimas para AWS

Configura `.env` en la EC2 con el endpoint de RDS, la base `dangoko`, el bucket privado y la región `us-west-2`. Para la exposición directa de AWS Academy por HTTP usa:

```dotenv
PREFERRED_URL_SCHEME=http
REQUIRE_AWS=true
REQUIRE_RDS=true
REQUIRE_NOTIFICATIONS=true
```

No subas `.env`, `terraform.tfvars`, tokens ni contraseñas. Usa `.env.example` como referencia.

## Redeploy seguro en la EC2

Desde `/opt/dangoko/repo`, conserva cualquier evidencia local y actualiza el código:

```bash
cd /opt/dangoko/repo
git fetch origin
git status --short
git merge --no-edit origin/main
sudo chown ec2-user:ec2-user .env
sudo chmod 600 .env
grep -q '^PREFERRED_URL_SCHEME=' .env && sed -i 's/^PREFERRED_URL_SCHEME=.*/PREFERRED_URL_SCHEME=http/' .env || echo 'PREFERRED_URL_SCHEME=http' >> .env
docker compose build --no-cache api
docker compose up -d --force-recreate api notifications
sleep 15
curl -i http://127.0.0.1:5000/salud
docker compose ps
```

Si `git merge` muestra conflictos, detén el redeploy y resuélvelos antes de reconstruir. No uses `git reset --hard` para conservar las evidencias generadas en la EC2.

## Cuenta y pedidos

La interfaz incluye registro e inicio de sesión visuales. Sus endpoints son:

```text
POST /api/auth/register
POST /api/auth/login
POST /api/auth/logout
GET  /api/auth/me
```

El checkout crea el pedido en RDS antes de notificar. Si falla la creación en RDS, responde `503` y no se envía ninguna notificación ni se presenta una confirmación exitosa. WhatsApp no se abre automáticamente en este avance.

## Validación de entrega

```bash
PYTHONPATH=app python -m pytest -q
python pipeline/run_pipeline.py --demo-red
python pipeline/run_pipeline.py
python pipeline/generate_sbom.py
bash verificar_entrega.sh
```
