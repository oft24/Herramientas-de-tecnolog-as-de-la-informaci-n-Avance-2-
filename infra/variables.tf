variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "bucket_name" {
  type        = string
  description = "Globally unique S3 bucket name"
}

variable "vpc_id" {
  type        = string
  description = "VPC where the application and RDS run"
}

variable "db_subnet_ids" {
  type        = list(string)
  description = "Private subnet IDs for the RDS subnet group"
}

variable "app_security_group_id" {
  type        = string
  description = "Security group ID attached to the application"
}

variable "db_identifier" {
  type    = string
  default = "dangoko-avance2"
}

variable "db_instance_class" {
  type    = string
  default = "db.t3.micro"
}

variable "db_name" {
  type    = string
  default = "dangoko"
}

variable "db_username" {
  type      = string
  sensitive = true
}

variable "db_password" {
  type      = string
  sensitive = true
}
