from pypelineer.cores import IngressCore, IngressType

import requests

from requests import Response
from typing import Any, Iterable, NoReturn, List

# Use Case 1: Functional Type Ingress
class ExtractTripadvisorURLs(IngressCore, Type=IngressType.FUNCTION):
    def constructor(self):
        URL = "https://raw.githubusercontent.com/sadigaxund/pypeliner/refs/heads/main/data/tripadvisor_urls.txt"
        response: Response = requests.get(URL)
        self.urls: List = response.text.splitlines()
        self.index = 0
    
    def destructor(self, exc_type, exc_value, traceback):
        del self.urls # Better practice: release memory
        # Moreover: Either ignore or log the exception
    
    def iterate(self) -> NoReturn:
        self.index += 1        
        
    def available(self) -> bool:
        return self.index + 1 < len(self.urls)
    
    def produce(self) -> Iterable | Any:
        return self.urls[self.index]
    
# Use Case 2: Input Type Ingress
class GenerateFibonacciSequences(IngressCore, Type=IngressType.INPUT):
    def constructor(self):
        self.memo = {}
        
    def destructor(self, exc_type, exc_value, traceback):
        del self.memo # Better practice: release memory
        # Moreover: Either ignore or log the exception
    
    def fibonacci(self, n):
        if n in self.memo:
            return self.memo[n]
        if n <= 1:
            return n
        self.memo[n] = self.fibonacci(n - 1) + self.fibonacci(n - 2)
        return self.memo[n]
        
    def produce(self) -> Iterable | Any:
        num = next(self.input)
        return (num, self.fibonacci(n=num))

def example_with_function():
    print("#" * 50)
    print("Use Case 1: Functional Type Ingress")
    with ExtractTripadvisorURLs() as tripadvisor_urls:
        for url in tripadvisor_urls:
            print(url)
            
def example_with_input():
    print("#" * 50)
    print("Use Case 2: Input Type Ingress")
    
    numbers = [4, 145, 53, 22, 4]
    
    with GenerateFibonacciSequences(input=numbers) as sequences:
        for sequence in sequences:
            print(sequence)


if __name__ == '__main__':
    example_with_function()
    example_with_input()