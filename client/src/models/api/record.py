import re
from dataclasses import dataclass, field
from typing import List, Union, Optional
from dataclass_type_validator import dataclass_type_validator
from lib.api.exceptions import OtherBadRequest
from datetime import datetime

@dataclass
class Record():
    bid: Union[str, int]
    rid: str
    rtt: Optional[str] = None
    sta: Optional[Union[datetime, str]] = None
    tid: Optional[Union[str, int]] = None
    def __post_init__(self):
        try:
            dataclass_type_validator(self)
        except Exception as e:
            raise OtherBadRequest(e.errors)

        # tid
        try:
            if self.tid is not None:
                self.tid = str(int(self.tid))
        except:
            raise OtherBadRequest("tid is auto-increased integer")

        # bid
        try:
            self.bid = str(int(self.bid))
        except:
            raise OtherBadRequest("bid is auto-increased integer")

        # sta (lending time)
        try:
            if type(self.sta) is datetime:
                self.sta = self.sta.strftime("%Y%m%d%H%M")
            elif type(self.sta) is str:
                self.sta = datetime.strptime(self.sta,"%Y%m%d%H%M")
                self.sta= self.sta.strftime("%Y%m%d%H%M")
        except Exception as e:
            raise OtherBadRequest("Time format should be like: 197001312359")
        
        
@dataclass
class Record_verbose(Record):
    tle: str = ""
    type: str = "reader"

    def __post_init__(self):
        try:
            dataclass_type_validator(self)
        except Exception as e:
            raise OtherBadRequest(e.errors)
        
        if self.type not in ["reader", "worker", "admin"]:
            raise OtherBadRequest("Invaild reader type. Must be reader, worker, or admin")