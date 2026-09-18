output "bucket_name" {
  value = aws_s3_bucket.orders.bucket
}

output "rds_endpoint" {
  value = aws_db_instance.app.address
}

output "rds_security_group_id" {
  value = aws_security_group.rds.id
}
