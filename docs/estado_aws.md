# Estado AWS — Dangoko Avance 2

## Fecha de prueba
2026-09-18

## Región
us-west-2

## Cuenta
943135209242

## EC2
- Name: dangoko-avance2-linux
- Instance ID: i-086d08e1bca370b0f
- IP pública: 44.251.176.246
- DNS: ec2-44-251-176-246.us-west-2.compute.amazonaws.com
- AZ: us-west-2b
- IAM Profile: LabInstanceProfile
- Commit activo: a0cde5e

## VPC y Red
- VPC: vpc-0fac5721d6511534a (172.31.0.0/16)
- Subnet EC2: subnet-0cb88dbc445e69b14 (us-west-2b)
- Subnet RDS 1: subnet-0cb88dbc445e69b14 (us-west-2b)
- Subnet RDS 2: subnet-039914022d6779c78 (us-west-2d)

## Security Groups
- App SG: dangoko-avance2-app-sg / sg-08fbe6a4ab91457cd
  - Ingress: TCP 22 y 5000 desde 0.0.0.0/0
  - Egress: todo
- RDS SG: dangoko-avance2-rds-sg / sg-073770a1042e0cb1d
  - Ingress: TCP 5432 solo desde sg-08fbe6a4ab91457cd
  - Sin acceso público

## S3
- Bucket: dangoko-avance2-943135209242-us-west-2-mkt
- Acceso público: BLOQUEADO (BlockPublicAcls, BlockPublicPolicy, IgnorePublicAcls, RestrictPublicBuckets)
- Cifrado: AES256
- Versionado: Enabled
- Objetos bajo orders/: 6 recibos guardados

## RDS
- Identifier: dangoko-avance2-rds
- Engine: postgres 16.15
- Endpoint: dangoko-avance2-rds.c8afxe8qtc3e.us-west-2.rds.amazonaws.com
- Puerto: 5432
- DB: dangoko
- Usuario: dangoko_admin
- publicly_accessible: false
- storage_encrypted: true
- Status: available

## Docker
- repo-api-1: healthy (puerto 5000)
- repo-db-1: healthy
- repo-notifications-1: healthy

## Prueba de /salud
- GET http://127.0.0.1:5000/salud → HTTP 200
- database_ready: true
- s3_ready: true

## Prueba de S3
- Objeto creado: orders/cdd59a1b-fbaa-4484-bc47-8d77b6241caa-99e7b626.json
- Tamaño: 398 bytes
- Timestamp: 2026-09-18T04:22:47Z

## Prueba de RDS
- users: 4 registros
- orders: 2 registros
- order_items: 2 registros
- Último pedido: BDK-FC80085E5B / Evidencia Final / $1120.00

## Prueba de Notificaciones
- POST /notifications/order HTTP 202 a las 04:22:47 UTC
- notification_status: sent

## Pipeline
- Corrida roja (--demo-red): DECISIÓN FINAL: BLOQUEADO
- Corrida verde: DECISIÓN FINAL: PERMITIDO

## Verificador
- Resultado: 13/15
- Pendiente 1: .env no se sube (correcto — está en .gitignore)
- Pendiente 2: video o enlace real (pendiente académico del estudiante)

## Comandos usados
- aws sts get-caller-identity
- aws ec2 describe-instances
- aws s3api get-public-access-block / get-bucket-encryption / list-objects-v2
- aws rds describe-db-instances
- aws ssm send-command / get-command-invocation
