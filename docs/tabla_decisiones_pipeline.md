# Tabla de decisiones de mi pipeline

Este pipeline termina en un solo veredicto. Una etapa fallida hace que la decisión sea `BLOQUEADO`, aunque las demás etapas pasen.

## Riesgos que introduce mi aplicación

| # | Riesgo concreto | Control | Por qué ese control |
|---|---|---|---|
| 1 | El catálogo recibe credenciales de AWS, RDS o Flask dentro del repositorio | Higiene de secretos | El API necesita acceso a S3 y RDS, por lo que una filtración permitiría leer recibos o modificar datos. |
| 2 | El bucket de recibos queda público o los pedidos de RDS quedan expuestos a Internet | Escaneo de IaC | El almacenamiento contiene datos de clientes y pedidos. El bloqueo público de S3 y `publicly_accessible = false` son propiedades verificables del código. |
| 3 | Una imagen Docker ejecuta la aplicación como root o sin comprobación de vida | Escaneo del Dockerfile | Un contenedor de API expuesto necesita reducir el impacto de una vulnerabilidad y permitir que Compose detecte un servicio no saludable. |
| 4 | Un cambio rompe el backend de catálogo o el flujo de pedido | Pruebas de sintaxis | La aplicación conserva mucho código heredado; compilar todos los módulos detecta errores baratos antes de construir o desplegar. |
| 5 | Se entrega el código sin inventario de dependencias | SBOM CycloneDX | Flask, boto3 y psycopg llegan desde terceros. El SBOM deja identificadas las versiones que deben revisarse. |

## Mis etapas y sus umbrales

| Etapa | Herramienta | Qué revisa | Umbral que bloquea | Por qué ese umbral |
|---|---|---|---|---|
| Pruebas de sintaxis y regresión | `compileall` + `unittest` | Módulos Python y pruebas del catálogo | Cualquier error de compilación o prueba fallida | Un módulo que no puede compilar o un flujo heredado que deja de funcionar no puede formar parte de una imagen funcional. |
| Higiene de secretos | `pipeline/run_pipeline.py` | Asignaciones no vacías de claves, contraseñas o llaves privadas | Cero hallazgos | Un solo secreto expuesto es suficiente para detener la entrega y rotarlo. |
| Infraestructura como código | `pipeline/run_pipeline.py` | Bloqueo público y cifrado de S3, cifrado y privacidad de RDS | Cualquier propiedad de seguridad ausente | Estos controles protegen directamente los datos de pedidos y son obligatorios en la consigna. |
| Docker endurecido | `pipeline/run_pipeline.py` | Imagen versionada, usuario no root y `HEALTHCHECK` | Cualquier control ausente | Son requisitos explícitos y reducen riesgos operativos básicos. |
| SBOM | `generate_sbom.py` | Dependencias fijadas de Python | SBOM ausente o sin formato CycloneDX | Sin inventario no se puede responder rápidamente a una vulnerabilidad de dependencia. |

## Lo que decidí no cubrir

| Riesgo que dejo fuera | Por qué lo dejo fuera | Qué haría con más tiempo |
|---|---|---|
| Pruebas dinámicas completas contra el contenedor | Primero se necesita estabilizar el MVP y contar con un entorno AWS levantado | Agregaría DAST autenticado y pruebas de contrato entre API y notificaciones. |
| Escaneo de vulnerabilidades de imagen con Trivy | Depende de tener el binario o la imagen de Trivy disponible en el entorno de ejecución | Añadiría Trivy con bloqueo en HIGH/CRITICAL y conservaría el reporte como evidencia. |
| Rotación automática de secretos | AWS Academy y el tiempo del avance no justifican implementar un gestor de secretos completo | Migraría credenciales a Secrets Manager y asignaría permisos mínimos por rol. |
