from pypelineer.cores import FunnelCore

from typing import Any
from pprint import pprint

class MergeFullname(FunnelCore):
    
    def aggregate(*records: Any) -> Any:
        return "Full Name: " + " ".join(records) 

def main():
    result = []
    result.append(MergeFullname.aggregate("Emily", "Carter"))
    result.append(MergeFullname.aggregate("Noah", "Bennett", "Smith"))
    result.append(MergeFullname.aggregate("Ava", "Thompson", "White", "Junior"))
    
    # Display
    print("Result:")
    pprint(result)
    
if __name__ == '__main__':
    main()