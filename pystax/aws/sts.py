import boto3

from pystax.aws import Sdk


class Sts(Sdk):
    def __init__(self):
        self.client = boto3.client("sts")
        self._id = None

    @property
    def id(self):
        if self._id is None:
            self._id = self.client.get_caller_identity()
        return self._id

    @property
    def account_id(self):
        return self.id.get("Account")

    @property
    def user_id(self):
        return self.id.get("UserId")

    @property
    def user_arn(self):
        return self.id.get("Arn")
