class Sdk:

    RETRY_LIMIT = 100

    # universal paginator for aws-sdk calls
    @staticmethod
    def paginate(method, **kwargs):
        client = method.__self__
        paginator = client.get_paginator(method.__name__)
        for page in paginator.paginate(**kwargs).result_key_iters():
            for result in page:
                yield result
