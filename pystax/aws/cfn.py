import boto3

from pystax.aws import Sdk


class Cfn(Sdk):

    # stack statuses that are not DELETE_COMPLETE
    STATUSES = [
        "CREATE_IN_PROGRESS",
        "CREATE_FAILED",
        "CREATE_COMPLETE",
        "ROLLBACK_IN_PROGRESS",
        "ROLLBACK_FAILED",
        "ROLLBACK_COMPLETE",
        "DELETE_IN_PROGRESS",
        "DELETE_FAILED",
        "UPDATE_IN_PROGRESS",
        "UPDATE_COMPLETE_CLEANUP_IN_PROGRESS",
        "UPDATE_COMPLETE",
        "UPDATE_ROLLBACK_IN_PROGRESS",
        "UPDATE_ROLLBACK_FAILED",
        "UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS",
        "UPDATE_ROLLBACK_COMPLETE",
        "REVIEW_IN_PROGRESS"
    ]
    
    COLORS = {
        # stack status
        "CREATE_COMPLETE":      "green",
        "DELETE_COMPLETE":      "green",
        "UPDATE_COMPLETE":      "green",
        "CREATE_FAILED":        "red",
        "DELETE_FAILED":        "red",
        "UPDATE_FAILED":        "red",
        "ROLLBACK_IN_PROGRESS": "red",
        "ROLLBACK_COMPLETE":    "red",
        # resource action
        "Add":    "green",
        "Modify": "yellow",
        "Remove": "red",
      }

    def __init__(self):
        self.client = boto3.client("cloudformation")

    def stacks(self):
        return [
            stack for stack in self.paginate(self.client.list_stacks, StackStatusFilter=self.STATUSES)
        ]
