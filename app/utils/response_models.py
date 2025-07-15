from typing import Any, Optional
from pydantic import BaseModel

class UnifiedResponse(BaseModel):
    success: bool
    code: int
    data: Optional[Any] = None
    message: str = ""

def success_response(data: Any = None, message: str = "Success", code: int = 200) -> UnifiedResponse:
    return UnifiedResponse(success=True, code=code, data=data, message=message)

def error_response(message: str = "Error", code: int = 500, data: Any = None) -> UnifiedResponse:
    return UnifiedResponse(success=False, code=code, data=data, message=message)