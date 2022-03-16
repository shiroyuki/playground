from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Message(BaseModel):
    id: Optional[str]
    author_id: Optional[str]
    content: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]