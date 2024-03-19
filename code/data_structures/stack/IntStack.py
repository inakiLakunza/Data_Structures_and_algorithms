from ListStack import ListStack
from ArrayStack import ArrayStack
from array import array as arr
from Stack import Stack


class IntStack(Stack):
  ''' 
  An integer implementation of a stack
  '''
  def __init__(self, maxSize):
    '''
    maxSize is the maximum number of items
    that can be in the queue at any given time
    ''' 
    self.pos = 0
    self.ar = arr('i', (0 for i in range(maxSize)))


  def size(self):
    """
    Returns the number of elements insize the stack
    """
    return self.pos


  def isEmpty(self):
    """
    Returns true/false on whether the stack is empty
    """
    return self.pos == 0


  def peek(self):
    if self.isEmpty():
      raise Exception('Empty Stack')
    return self.ar[self.pos - 1]


  def push(self, value):
    """
    Add an element to the top of the stack
    """
    self.ar[self.pos] = value
    self.pos += 1


  def pop(self):
    """
    Make sure you check that the stack is not empty before calling pop!
    """
    if self.isEmpty():
      raise Exception('Empty Stack')
    self.pos -= 1
    return self.ar[self.pos]
