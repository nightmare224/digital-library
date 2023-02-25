from dataclasses import dataclass, field
from typing import List, Union, Optional
from dataclass_type_validator import dataclass_type_validator
from lib.api.exceptions import OtherBadRequest


@dataclass
class Reader():
    rid: str 
    tle: str
    type: str = "reader"
    
    def __post_init__(self):
        try:
            dataclass_type_validator(self)
        except Exception as e:
            raise OtherBadRequest(e.errors)
        
        if self.type not in ["reader", "worker", "admin"]:
            raise ValueError("Invaild reader type. Must be reader, worker, or admin")