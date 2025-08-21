#!/bin/sh
set -e

# Wait for MinIO to be ready and configure alias
until mc alias set "$MINIO_ALIAS" "$MINIO_URL" "$MINIO_ACCESS_KEY" "$MINIO_SECRET_KEY"; do
  echo "Waiting for MinIO..."
  sleep 2
done

# Split the env var into an array
IFS=',' read -r -a buckets <<< "$MINIO_BUCKETS"

for bucket in "${buckets[@]}"; do
  mc mb --ignore-existing "$MINIO_ALIAS/$bucket"
  echo "Bucket $bucket ensured"
done
