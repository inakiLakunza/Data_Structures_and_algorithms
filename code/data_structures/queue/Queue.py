

from abc import ABC,abstractmethod 


# As in languages as Java, we will create and abstract class and define
# the methods that will be necessary to implement when inheriting 
# from this parent class
class Queue(ABC):

  @abstractmethod
  def offer(self, elem):
    pass

  @abstractmethod
  def poll(self):
    pass

  @abstractmethod
  def peek(self):
    pass

  @abstractmethod
  def size(self):
    pass

  @abstractmethod
  def isEmpty(self):
    pass