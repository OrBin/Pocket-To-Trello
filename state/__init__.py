import os

from state.interface import StateManager
from state.local_file import LocalFileStateManager
from state.s3 import S3StateManager


def select_state_manager() -> StateManager:
    state_s3_bucket = os.getenv("STATE_S3_BUCKET")
    if state_s3_bucket is not None:
        aws_region = os.getenv("AWS_REGION")
        assert aws_region, "Must specify AWS_REGION when storing state in S3"
        return S3StateManager(state_s3_bucket, aws_region)

    return LocalFileStateManager()
