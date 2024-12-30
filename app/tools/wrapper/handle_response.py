from app.tools.response import Response


def handle_response(func):
    def wrapper(self, *args, **kwargs):
        try:
            res = func(self, *args, **kwargs)
            if isinstance(res, Response):
                return res
            else:
                return Response.success(response=res)
        except Exception as e:
            return Response.fail(str(e))

    return wrapper
