from abc import ABC, abstractmethod


class AbstractClassExample(ABC):
    @abstractmethod
    def another_abstract_method(self, parameter):
        pass

    def concrete_method(self):
        print("This is a concrete method in the abstract class.")

# Attempting to instantiate an abstract class will raise an error
# obj = AbstractClassExample()  # This line will raise an error

# Subclassing the abstract class and implementing abstract methods


class ConcreteClass(AbstractClassExample):

    def another_abstract_method(self, parameter):
        print(
            f"Implementation of another_abstract_method with parameter: {parameter}")


# Now, you can create an instance of the concrete class
obj = ConcreteClass()
obj.another_abstract_method("example")
obj.concrete_method()
