# Dangoko Marketplace Avance 2

Avance 2 de LSCA2314. Esta aplicación parte del catálogo mayorista de Bbldak y lo adapta a un marketplace pequeño para dangokobox.com. Un visitante puede consultar el catálogo, crear una cuenta, iniciar sesión y generar un pedido de cotización. El pedido se guarda en PostgreSQL/RDS, su recibo JSON se almacena en un bucket privado de S3 y un servicio independiente registra la notificación de confirmación.

Datos académicos pendientes de captura: nombre completo y matrícula del alumno. Tema elegido: 3, Marketplace. Repositorio de entrega: `https://github.com/oft24/Herramientas-de-tecnolog-as-de-la-informaci-n-Avance-2-.git`.

## Cómo se levanta en desarrollo

```powershell
Copy-Item .env.example .env
docker compose up --build
```

La aplicación queda en `http://localhost:5000`. El endpoint de salud es `GET /salud`. El servicio de notificaciones vive en `http://localhost:5001` dentro de Compose y PostgreSQL local reemplaza a RDS solamente durante el desarrollo.

## Flujo principal

1. El frontend muestra el catálogo heredado de Bbldak.
2. `POST /api/auth/register` y `POST /api/auth/login` identifican al usuario mediante una sesión Flask.
3. `POST /api/checkout` valida productos, cantidades y consentimiento.
4. El API guarda el pedido y sus partidas en PostgreSQL.
5. El API escribe un recibo privado en S3 con cifrado AES256.
6. El API llama a `notifications` por HTTP. Ese contenedor registra la confirmación en un archivo de eventos.

## Servicios de AWS

| Servicio | Uso | Controles definidos |
|---|---|---|
| S3 | Recibos JSON de los pedidos | Bloqueo total de acceso público, cifrado AES256 y versionado |
| RDS PostgreSQL | Usuarios, pedidos y partidas | Cifrado de almacenamiento, `publicly_accessible = false`, subredes privadas y grupo de seguridad que solo permite tráfico desde la aplicación |

Terraform deja la configuración en `infra/`. Los valores sensibles se proporcionan por variables o por el entorno de AWS Academy; no se guardan en Git.

## Variables importantes

En el despliegue real se deben establecer `DB_HOST` con el endpoint de RDS, `DB_SSLMODE=require`, `S3_BUCKET`, `AWS_REGION`, `FLASK_SECRET_KEY`, las credenciales de AWS mediante el mecanismo seguro disponible y `REQUIRE_RDS=true`, `REQUIRE_AWS=true`. Para la práctica local se usan los valores de `.env.example` y el contenedor `db`.

## Pipeline

```powershell
python pipeline/run_pipeline.py
```

El pipeline ejecuta pruebas de sintaxis, higiene de secretos, controles de IaC, endurecimiento del Dockerfile y generación de SBOM CycloneDX. Todas las etapas alimentan un único veredicto. El modo rojo para la evidencia usa un candidato temporal con una asignación de secreto:

```powershell
python pipeline/run_pipeline.py --demo-red *> reportes/corrida_roja.txt
python pipeline/run_pipeline.py *> reportes/corrida_verde.txt
```

## Estado de entrega

La aplicación, Docker, Terraform, pipeline y documentación técnica están preparados. Falta completar con datos personales, crear los recursos reales en AWS Academy, configurar las variables, capturar las ocho evidencias, grabar el video de 3 a 5 minutos y subir el commit al repositorio destino.
