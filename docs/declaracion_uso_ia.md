# Declaración de uso de inteligencia artificial

Usé Codex como apoyo para leer las instrucciones, revisar Bbldak, proponer la separación de servicios y escribir una primera versión del código. La responsabilidad de entender, probar y corregir cada parte sigue siendo del alumno.

## Qué generé con ayuda de IA

| Parte | Herramienta | Qué le pedí | Qué debo verificar o cambiar yo |
|---|---|---|---|
| Adaptación del backend | Codex | Convertir el checkout en un flujo de marketplace con usuarios, pedidos y notificaciones | Probar registro, login, pedido y errores con datos propios |
| Docker Compose | Codex | Separar API, notificaciones y PostgreSQL | Confirmar nombres, puertos, volúmenes y credenciales locales |
| Terraform | Codex | Describir S3 privado y RDS PostgreSQL sin acceso público | Completar VPC, subredes, grupo de seguridad y límites de AWS Academy |
| Pipeline y documentación | Codex | Crear controles, SBOM y documentos de la plantilla | Ejecutar el pipeline, conservar evidencia real y explicar las decisiones en el video |

## Qué hice sin IA

Elegí reutilizar Bbldak como base, seleccioné el tema Marketplace, decidí que la pieza distintiva sería el servicio de notificaciones y debo validar personalmente la cuenta AWS, las variables, los resultados del pipeline y las capturas de entrega.

## Algo que la IA me dio mal y tuve que corregir

La primera integración dejó una inconsistencia entre el identificador público del pedido y el UUID usado en la base de datos, además de una referencia incorrecta al producto al insertar las partidas. Se corrigió separando `public_order_id`, `order_id` y `product_id`, y revisando el contrato de cada función. Debo confirmar este caso con una prueba real antes de entregar.
