from game import *

b = Board(5, 10)
s1 = Block(1)
s2 = Block(2)
b.addBlock(s1, 1 ,1)
print(b)
b.removeRow(9)
print(b)
b.addBlock(s2, 1 ,1)
print(b)
