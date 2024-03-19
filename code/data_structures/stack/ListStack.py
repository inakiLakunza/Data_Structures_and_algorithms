import sys
sys.path.insert(0, "./../linked_lists")

from Stack import Stack
# Using the DOubly linked list we created
from Doubly_linked_list_sc import DoublyLinkedList

class ListStack(Stack):
  ''' 
  A linked list implementation of a stack
  '''
  def __init__(self):

    # Create a doubly linked list, and the iterator
    # we will use to move along it
    self.list = DoublyLinkedList()
    self.iterList = iter(self.list)


  def size(self):
    '''
    Return the number of elements in the stack    
    ''' 
    # The size of the stack is just the size of
    # our doubly linked list
    return self.list.size()


  def isEmpty(self):
    """
    Check if the stack is empty
    """
    return self.size() == 0


  def push(self, elem):
    """
    Push an element on the stack
    """
    # We will insert element at the back
    # of the list, and pop from there
    self.list.addLast(elem)


  def pop(self):
    """
    Pop an element off the stack
    Throws an error is the stack is empty
    """
    if self.isEmpty():
      raise Exception('Empty Stack')
    return self.list.removeLast()


  def peek(self):
    """
    Peek the top of the stack without removing an element
    Throws an exception if the stack is empty
    """
    if self.isEmpty():
      raise Exception('Empty Stack')
    return self.list.peekLast()


  def __iter__(self): 
    """
     Called when iteration is initialized
    """
    self.iterList = iter(self.list)
    return self


  def __next__(self): 
    """
    To move to next element. 
    """  
    return next(self.iterList)