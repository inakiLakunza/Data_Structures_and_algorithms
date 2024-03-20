from Queue import Queue

class ArrayQueue(Queue):
  ''' 
  An array implementation of a queue
  '''
  # we will set a maximum size since we will be using
  # a static array. We will create the array, which will
  # be a list in this case, and the head and tail pointers
  def __init__(self, obj, capacity): 
    self.qSize = 0
    self.data = [obj for i in range(capacity)]
    self.front = 0
    self.rear = 0


  def size(self):
    return self.adjustIndex(self.rear + len(self.data) - self.front, len(self.data))


  def offer(self, elem):
    if self.isFull():
      raise Exception('Queue is full')

    # When enqueuing, we have to add another element at the back
    # and move the tail pointer forward
    self.data[self.rear] = elem
    self.rear += 1
    self.rear = self.adjustIndex(self.rear, len(self.data))


  def poll(self):
    if self.isEmpty():
      raise Exception('Queue is empty')
    
    # When dequeuing we have to do just the contrary of enqueuing,
    # we have to move our head pointer forward and in other languages
    # we have to deallocate the memory
    self.front = self.adjustIndex(self.front, len(self.data))
    d = self.data[self.front]
    self.front += 1
    return d


  def peek(self):
    if self.isEmpty():
      raise Exception('Queue is empty')
    self.front = self.adjustIndex(self.front, len(self.data))
    return self.data[self.front]


  def isEmpty(self):
    return self.rear == self.front


  def isFull(self):
    return (self.front + len(self.data) - self.rear) % len(self.data) == 1


  def adjustIndex(self, index, size):
    return index - size if index >= size else index
