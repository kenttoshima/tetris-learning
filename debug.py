from game import *

b = Board(5, 10)
s = Block(1)
b.addBlock(s, 1 ,1)
print(b)
b.removeRow(9)
print(b)
b.addBlock(s, 1 ,1)
print(b)
