import sys
from Stack import Stack


class ArrayStack(Stack):
  ''' 
  An array implementation of a stack
  '''
  def __init__(self, obj): 
    self.stkSize = 0
#    self.capacity = 16
    self.data = [] #[obj for i in range(self.capacity)]
    self.initSize = sys.getsizeof(self.data)
    


  def size(self):
    return self.stkSize


  def isEmpty(self):
    return self.stkSize == 0


  def push(self, elem):
    self.data.append(elem)
    self.stkSize += 1
    spaceLeft = ((sys.getsizeof(self.data) - self.initSize) - len(self.data) * 8) // 8
    print("space left after append: ", spaceLeft)


  def pop(self):
    if self.isEmpty():
      raise Exception('Empty Stack')
    self.stkSize -= 1
    elem = self.data[self.stkSize]

#    spaceLeft = ((sys.getsizeof(self.data) - self.initSize) - len(self.data) * 8) // 8
#    print("space left before pop: ", spaceLeft)

#    self.data[self.stkSize] = None
    elem = self.data.pop(self.stkSize)

#    spaceLeft = ((sys.getsizeof(self.data) - self.initSize) - len(self.data) * 8) // 8
#    print("space left after pop: ", spaceLeft)

    return elem


  def peek(self):
    if self.isEmpty():
      raise Exception('Empty Stack')
    
    return self.data[self.stkSize - 1]