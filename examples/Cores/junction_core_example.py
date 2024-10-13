from pypelineer.cores import JunctionCore

from typing import Any, Tuple
from pprint import pprint

class DivideFullname(JunctionCore):
    
    def segregate(record: Any) -> Tuple[Any]:
        return record['first_name'], record['last_name']    

def main():
    
    data = [
        {"first_name": "Emily", "last_name" : "Carter"},
        {"first_name": "Noah", "last_name" : "Bennett"},
        {"first_name": "Ava", "last_name" : "Thompson"},
    ]
    
    result = []
    for e in data:
        result.append(DivideFullname.segregate(e))
    
    # Display
    print("Result:")
    pprint(result)
    
if __name__ == '__main__':
    main()