from typing import Optional
from pydantic import BaseModel

#Un esquema de pydantic
class TokenData(BaseModel):
    username: Optional[str] = None