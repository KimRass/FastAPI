from pydantic import BaseModel
from typing import List


class UserInput(BaseModel):
    nums: List[int] = list(range(10))
    batch_size: int = 1
