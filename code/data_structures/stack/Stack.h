#ifndef D_STACK_H
#define D_STACK_H

#include <deque>
#include <list>
#include <set>   // set and multiset
#include <map>   // map and multimap
#include <unordered_set>  // unordered set/multiset
#include <unordered_map>  // unordered map/multimap
#include <iterator>
#include <algorithm>
#include <numeric>    // some numeric algorithm
#include <functional>
#include <stack>

#include <sstream>
#include <memory>
#include <iostream>
#include <stdexcept>

namespace dsa {

template <typename T>
class Stack
{
private:
  int id_;

public:
  Stack(int id) : id_(id) {}

  virtual ~Stack() {}

  // return the ID the stack implementation
  virtual int id() { return id_; }

  // return the number of elements in the stack
  virtual int size() = 0;

  // clear the stack
  virtual void clear() = 0;

  // return if the stack is empty
  virtual bool isEmpty() = 0;

  // push the element on the stack
  virtual void push(T elem) = 0;

  // pop the element off the stack
  virtual T pop() = 0;

  virtual T peek() = 0;
};

} // namespace dsa

#endif /* D_STACK_H */