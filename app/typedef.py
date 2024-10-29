""" 
Module for dataclasses
"""

from dataclasses import dataclass
from datetime import datetime

from yarl import URL


@dataclass
class Lookalike:
    neighbor_url: str
    distance: float
    title: str
    id: str
    published_date: datetime
