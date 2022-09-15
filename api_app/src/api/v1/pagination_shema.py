from typing import Optional

from pydantic import BaseModel


class PaginationSchema(BaseModel):
    page_size: Optional[int] = 50
    page_number: Optional[int] = 1
