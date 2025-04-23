from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PaginatedResponse[T](BaseModel):
    items: list[T]
    next_cursor: Optional[datetime]
    total_count: int