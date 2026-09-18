# Herramientas de tecnologías de la información Avance 2

Proyecto de Avance 2 de LSCA2314. La aplicación parte de Bbldak/dangokobox y se adapta al tema 3, Marketplace, con un servicio independiente de notificaciones.

La documentación de entrega está en [docs/README.md](docs/README.md). La implementación principal vive en `app/`; la infraestructura está en `infra/`; el pipeline y sus controles están en `pipeline/`.

## Inicio rápido

```powershell
Copy-Item .env.example .env
docker compose up --build
```

Antes de una entrega ejecuta el pipeline y el verificador descritos en la documentación.
