from fastapi import HTTPException

class LLMException:
    class FailedCallbck(HTTPException):
        def __init__(self, detail: str = "Callback server returned an error"):
            super().__init__(status_code=502, detail=detail)

    class APIError(HTTPException):
        def __init__(self, detail: str = "OpenAI API Error"):
            super().__init__(status_code=500, detail=detail)

    class UnexpectedError(HTTPException):
        def __init__(self, detail: str = "Unexpected Error in LLM Service"):
            super().__init__(status_code=500, detail=detail)