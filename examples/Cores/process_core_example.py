from pypelineer.cores import ProcessCore, processor

from typing import Dict
from pprint import pprint
import datetime

class TransformData(ProcessCore):
    '''
    Rules:
    1. The function to be applied to the data should be decorated with 'processor'.
    2. Naming is flexible: function names, parameter names, and type definitions can be anything.
    3. Automatic overloading is applied; as long as the function is decorated with 'processor', multiple functions with the same name can coexist. 
    4. All processors are applied to the data sequentially from top to bottom, including overloaded functions.
    5. The first parameter of the function will be the one that is processed.
    6. Always return the processed data, otherwise output will be nulls.
    '''
    ID_POOL = 0
    
    @processor 
    def assign_id(data: Dict):
        data['id'] = TransformData.ID_POOL
        TransformData.ID_POOL += 1
        return data
    
    @processor 
    def add_timestamp(data: Dict):
        data['timestamp'] = datetime.datetime.now().timestamp()
        return data
    
    @processor
    def process(data: Dict):
        data['value'] = int(data['value'] / 2)
        return data
        
    @processor
    def process(data: Dict):
        data['value'] += 3
        return data

def main():
    data = [
        {"value": 2},
        {"value": 4},
        {"value": 6},
        {"value": 8},
        {"value": 10},
    ]
    
    core = TransformData()
    # Simpler:
    # result = list(map(core.process, data))
    
    # Or:
    result = []
    for e in data:
        result.append(core.process(e))
    
    # Display
    print("Result:")
    pprint(result)

if __name__ == '__main__':
    main()