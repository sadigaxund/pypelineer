from .....cores.implement.process import *

import json

class AnyJSONEncodeCore(Core):

    @processor
    def encode(listing: dict) -> bytearray:
        json_record = json.dumps(
            obj=listing,
            ensure_ascii=False,
            default=str
        )
        
        byte_record = json_record.encode('utf-8')
        
        return byte_record