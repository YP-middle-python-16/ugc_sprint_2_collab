from pydantic import BaseModel
from typing import Optional


class PaginationSchema(BaseModel):
    page_size: Optional[int] = 50
    page_number: Optional[int] = 1
