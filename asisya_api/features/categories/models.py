from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class CategoryCreateDTO:
    name: str
    slug: Optional[str] = None
    description: Optional[str] = None
    picture_path: Optional[str] = None


@dataclass
class CategoryResponseDTO:
    id: int
    name: str
    slug: Optional[str]
    description: Optional[str]
    picture_url: Optional[str]
    created_at: datetime
    updated_at: datetime
