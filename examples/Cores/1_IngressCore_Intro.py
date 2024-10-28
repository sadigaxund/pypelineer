'''
    www.youtube.com/@Pypelineer
'''

from pypelineer.cores import IngressCore, IngressType

class OddorEvenNumber(IngressCore, Type=IngressType.INPUT):
    
    def __init__(self, numbers: list):
        super().__init__(input = numbers)
    
    def produce(self):
        number = next(self.input)
        
        if number % 2 == 0:
            return number, "Even"
        else:
            return number, "Odd"

if __name__ == '__main__':
    
    numbers = [1, 2, 3, 4, 5]

    oddity = OddorEvenNumber(numbers)
    oddity.constructor()
    
    for number, odd_or_even in oddity:
        print(f"Number '{number}' is {odd_or_even}")
        
