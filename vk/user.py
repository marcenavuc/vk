from dataclasses import dataclass
from typing import Dict


@dataclass
class User:
    id: int
    first_name: str
    last_name: str
    count: int

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(data.get("id", -1),
                   data.get("first_name", ""),
                   data.get("last_name", ""),
                   data.get("count", -1))

    def __str__(self):
        return "{} {} {} {}".format(self.id, self.first_name,
                                    self.last_name, self.count)
