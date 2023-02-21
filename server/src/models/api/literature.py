import re
from dataclasses import dataclass, field
from typing import List, Union, Optional
from dataclass_type_validator import dataclass_type_validator
from lib.api.exceptions import OtherBadRequest


@dataclass
class Literature():
    tle: str
    type: str
    bid: Optional[Union[str, int]] = None
    def __post_init__(self):
        try:
            dataclass_type_validator(self)
        except Exception as e:
            raise OtherBadRequest(e.errors)
        # bid
        try:
            if self.bid is not None:
                self.bid = str(int(self.bid))
        except:
            raise OtherBadRequest("bid is auto-increased integer")