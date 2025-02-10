from fastapi import HTTPException

class GlobalException:
    class UnprocessableEntity(HTTPException):
        def __init__(self, detail: str):
            super().__init__(status_code=422, detail=detail)
    
    class NotFound(HTTPException):
        def __init__(self, detail: str):
            super().__init__(status_code=404, detail=detail)

    class InternalServerError(HTTPException):
        def __init__(self, detail: str):
            super().__init__(status_code=500, detail=detail)

    class TooManyRequests(HTTPException):
        def __init__(self, detail: str):
            super().__init__(status_code=429, detail=detail)
    
    