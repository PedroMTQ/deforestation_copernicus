from deforestation_copernicus.io.logger import logger
from minio import Minio
from minio.datatypes import Object
from minio.error import S3Error
from retry import retry
from deforestation_copernicus.settings import (MINIO_ENDPOINT,
                                               MINIO_ROOT_USER,
                                               MINIO_ROOT_PASSWORD,
                                               MINIO_WRITE_RETRIES,
                                               MINIO_WRITE_RETRY_BACKOFF,
                                               MINIO_WRITE_RETRY_DELAY)


MINIO_RETRY_EXCEPTIONS = (S3Error,)



class ClientMinio:
    def __init__(self,
                 bucket_name: str,
                 endpoint=MINIO_ENDPOINT,
                 access_key=MINIO_ROOT_USER,
                 secret_key=MINIO_ROOT_PASSWORD):
        self.endpoint = endpoint
        self.__access_key = access_key
        self.__secret_key = secret_key
        self.bucket_name = bucket_name
        logger.debug(f'Trying to connect to minio at {self.endpoint}')
        self.__connect()
        logger.debug(f'Connected to minio at {self.endpoint}')

    def __connect(self):
        try:
            self.client = Minio(endpoint=self.endpoint,
                                access_key=self.__access_key,
                                secret_key=self.__secret_key,
                                secure=False
                                )
            self.ping()
        except Exception as e:
            raise ConnectionError(f"Unable to connect to MinIO at {self.endpoint}. Exception: {e}") from e

    def ping(self):
        self.client.bucket_exists("nonexistingbucket")


    def create_bucket(self):
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
        except Exception as e:
            raise ConnectionError(f"Unable to create or verify bucket {self.bucket_name}.") from e

    @retry(exceptions=MINIO_RETRY_EXCEPTIONS,
           tries=MINIO_WRITE_RETRIES,
           delay=MINIO_WRITE_RETRY_DELAY,
           backoff=MINIO_WRITE_RETRY_BACKOFF,
           logger=logger)
    def upload_file(self, file_path: str, object_name: str):
        try:
            logger.info(f"Uploading {file_path} to bucket {self.bucket_name} as {object_name}")
            self.client.fput_object(bucket_name=self.bucket_name,
                                    object_name=object_name,
                                    file_path=file_path)
        except Exception:
            logger.error(f"Failed to upload {file_path} to {self.bucket_name}/{object_name}")
            raise

    @retry(exceptions=MINIO_RETRY_EXCEPTIONS,
           tries=MINIO_WRITE_RETRIES,
           delay=MINIO_WRITE_RETRY_DELAY,
           backoff=MINIO_WRITE_RETRY_BACKOFF,
           logger=logger)
    def delete_file(self, object_name: str):
        try:
            logger.info(f"Deleting {object_name} from bucket {self.bucket_name}")
            self.client.remove_object(bucket_name=self.bucket_name, object_name=object_name)
        except Exception as e:
            logger.error(f"Failed to delete {object_name} from bucket {self.bucket_name} due to {e}")


    @retry(exceptions=MINIO_RETRY_EXCEPTIONS,
           tries=MINIO_WRITE_RETRIES,
           delay=MINIO_WRITE_RETRY_DELAY,
           backoff=MINIO_WRITE_RETRY_BACKOFF,
           logger=logger)
    def download_file(self, object_name: str, file_path: str):
        try:
            logger.info(f"Downloading {object_name} from bucket {self.bucket_name} to {file_path}")
            self.client.fget_object(bucket_name=self.bucket_name,
                                    object_name=object_name,
                                    file_path=file_path
                                    )
        except Exception as e:
            logger.error(f"Failed to download {object_name} from {self.bucket_name} to {file_path}")
            raise e


    @retry(exceptions=MINIO_RETRY_EXCEPTIONS,
           tries=MINIO_WRITE_RETRIES,
           delay=MINIO_WRITE_RETRY_DELAY,
           backoff=MINIO_WRITE_RETRY_BACKOFF,
           logger=logger)
    def get_objects(self, prefix: str = "") -> list[Object]:
        try:
            objects = self.client.list_objects(bucket_name=self.bucket_name, prefix=prefix, recursive=True)
            return [obj for obj in objects]
        except Exception:
            logger.error(f"Failed to list objects in bucket {self.bucket_name} with prefix '{prefix}'")
            raise


    @retry(exceptions=MINIO_RETRY_EXCEPTIONS,
           tries=MINIO_WRITE_RETRIES,
           delay=MINIO_WRITE_RETRY_DELAY,
           backoff=MINIO_WRITE_RETRY_BACKOFF,
           logger=logger)
    def get_object(self, object_name: str) -> Object | None:
        """Generate a presigned URL to access the object."""
        try:
            return self.client.stat_object(self.bucket_name, object_name)
        except Exception as e:
            logger.debug(f'Could not find object {object_name} due to {e}')

if __name__ == '__main__':
    connector = ClientMinio(bucket_name='satellite-data')
    # Example usage
    print(connector.get_object('test'))
