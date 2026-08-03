class Person:

    name:str
    age:int
    height:int|float
    weight:int|float

    def __init__(self,name:str,age:int,height:int|float,weight:int|float):
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight


    def info(self) -> str:
        return f"{self.name}, {self.age}, {self.height}, {self.weight}"


    def bmi(self) -> float:
        return self.weight / (self.height ** 2)

    def __str__(self) -> str:
        return f"{self.name}, {self.age}, {self.height}, {self.weight}"

    def __repr__(self) -> str:
        return f"{self.name}, {self.age}, {self.height}, {self.weight}"

