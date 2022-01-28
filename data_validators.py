from pydantic import BaseModel
from typing import Optional


class ClassesValidation(BaseModel):
    class_id: Optional[int] = None
    class_name: str
    class_short: str
