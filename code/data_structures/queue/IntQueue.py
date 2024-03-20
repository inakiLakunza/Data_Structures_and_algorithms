from array import array as arr
from collections import deque
from Queue import Queue


class IntQueue(Queue):
  ''' 
  An integer only implementation of a queue
  '''
  # We will only use integers
  # We will define a maximum size for our queue
  # since we will be using an analogous to an static array
  # We wull have a pointer pointing to the head
  # and a pointer pointing to the tail, and at
  # the beginning they will be 0
  def __init__(self, maxSize):
    """
    maxSize is the maximum number of items
    that can be in the queue at any given time
    """ 
    self.front = 0
    self.end = 0
    self.qSize = 0
    self.data = arr('i', (0 for i in range(maxSize)))


  def isEmpty(self):
    """
    Return true/false on whether the queue is empty
    """
    return self.qSize == 0


  def size(self):
    """
    Return the number of elements inside the queue
    """  
    return self.qSize


  def peek(self):
    if self.isEmpty():
      raise Exception('Queue is empty')
      
    self.front = self.front % len(self.data)
    return self.data[self.front]


  def isFull(self):
    return self.qSize == len(self.data)


  def offer(self, value):
    """
    Add an element to the queue
    """
    if self.isFull():
      raise Exception("Queue too small!")
    
    # When enqueuing and element, we have to first
    # check if the queue is full. Otherwise we 
    # have to add a value at the back and move our
    # tail pointer to the next element (the new tail)
    self.data[self.end] = value
    self.end += 1
    self.qSize += 1
    self.end = self.end % len(self.data)


  def poll(self):
    """
    Make sure you check is the queue is not empty before calling poll!
    """
    if self.isEmpty():
      raise Exception('Queue is empty')
    
    # After checking that the queue is not empty, we will move
    # our head pointer to the next element (and in other languages)
    # it will be necessary to set the dequeued element to null
    # so that we can clean up the memory.
    self.qSize -= 1
    self.front = self.front % len(self.data)
    d = self.data[self.front]
    self.front += 1
    return d
