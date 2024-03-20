import sys
sys.path.insert(0, "./../linked_lists")

from Queue import Queue
from Doubly_linked_list_sc import DoublyLinkedList

# We will use the created DoublyLinkedList for creating a queue
class LinkedQueue(Queue):
  ''' 
  A linked list implementation of a queue
  '''
  def __init__(self): 
    # Intialize the Doubly linked list and create the iterator
    self.list = DoublyLinkedList()
    self.iterList = iter(self.list)


  def size(self):
    """
    Return the size of the queue
    """
    # The same of the queue will be the size of the 
    # Doubly Linked List
    return self.list.size()


  def isEmpty(self):
    """
    Returns whether or not the queue is empty
    """
    return self.size() == 0


  def peek(self):
    """
    Peek the element at the front of the queue
    The method throws an error is the queue is empty
    """
    if self.isEmpty():
      raise Exception('Queue Empty')
    return self.list.peekFirst()


  def poll(self):
    """
    Poll an element from the front of the queue
    The method throws an error is the queue is empty
    """
    # We will dequeue, removing the first element
    # in the DOubly Linked List, we can do this
    # just by using the remove first element
    # method that we created when creating the
    # Doubly Linked List class
    if self.isEmpty():
      raise Exception('Queue Empty')
    return self.list.removeFirst()


  def offer(self, elem):
    """
    Add an element to the back of the queue
    """
    self.list.addLast(elem)


  def __iter__(self): 
    """
     Called when iteration is initialized

     Return an iterator to allow the user to traverse
     through the elements found inside the queue
    """
    self.iterList = iter(self.list)
    return self


  def __next__(self): 
    """
    To move to next element. 
    """  
    return next(self.iterList)
