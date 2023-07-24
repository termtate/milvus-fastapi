from functools import cached_property
from dataclasses import dataclass

@dataclass
class A:
    a: int
    
    @cached_property
    def b(self):
        print(11)
        return self.a + 1


a = A(1)

print(a.b)

a.a = 2

print(a.b)

