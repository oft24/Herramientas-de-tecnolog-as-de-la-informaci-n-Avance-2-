terraform {
  required_version = ">= 1.8.0, < 2.0.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.70"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_s3_bucket" "orders" {
  bucket        = var.bucket_name
  force_destroy = false

  tags = {
    Project = "dangoko-avance2"
    Purpose = "private-order-receipts"
  }
}

resource "aws_s3_bucket_public_access_block" "orders" {
  bucket                  = aws_s3_bucket.orders.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "orders" {
  bucket = aws_s3_bucket.orders.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_versioning" "orders" {
  bucket = aws_s3_bucket.orders.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_db_subnet_group" "app" {
  name       = "dangoko-avance2-db-subnets"
  subnet_ids = var.db_subnet_ids
  tags       = { Project = "dangoko-avance2" }
}

resource "aws_security_group" "rds" {
  name        = "dangoko-avance2-rds"
  description = "Only the application security group may reach PostgreSQL"
  vpc_id      = var.vpc_id

  ingress {
    description     = "PostgreSQL from the application"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [var.app_security_group_id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_db_instance" "app" {
  identifier              = var.db_identifier
  engine                  = "postgres"
  engine_version          = "16.4"
  instance_class          = var.db_instance_class
  allocated_storage       = 20
  max_allocated_storage   = 50
  storage_type            = "gp3"
  storage_encrypted       = true
  db_name                 = var.db_name
  username                = var.db_username
  password                = var.db_password
  port                    = 5432
  publicly_accessible     = false
  multi_az                = false
  skip_final_snapshot     = true
  deletion_protection     = false
  db_subnet_group_name    = aws_db_subnet_group.app.name
  vpc_security_group_ids  = [aws_security_group.rds.id]
  backup_retention_period = 1
  apply_immediately       = true

  tags = {
    Project = "dangoko-avance2"
    Purpose = "marketplace-data"
  }
}
