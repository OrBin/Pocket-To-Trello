import boto3
import botocore

from state.interface import StateManager


OBJECT_KEY = "pocket_last_checked.txt"


class S3StateManager(StateManager):
    def __init__(self, bucket_name: str, region: str):
        s3 = boto3.resource('s3', region_name=region)
        bucket = s3.Bucket(bucket_name)
        self._state_object = bucket.Object(OBJECT_KEY)

    def _exists(self) -> bool:
        try:
            self._state_object.load()
            return True
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                return False
            else:
                raise

    def _read(self) -> str:
        resp = self._state_object.get()
        return resp['Body'].read().decode()

    def write(self, new_state: str):
        self._state_object.put(Body=new_state.encode())
