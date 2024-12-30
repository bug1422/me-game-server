class Response:
    def __init__(self, result: bool, message: str, response: object):
        self.result = result
        self.message = message
        self.response = response

    @classmethod
    def success(cls, message: str = "Action success", response: object = None):
        return Response(True, message, response)

    @classmethod
    def fail(cls, message: str = "Action unsuccess", response: object = None):
        return Response(False, message, response)
