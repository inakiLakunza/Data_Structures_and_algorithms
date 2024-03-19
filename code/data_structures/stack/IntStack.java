public class IntStack implements Stack<Integer> {

  private int[] ar;
  private int pos = 0;

  // maxSize is the maximum number of items
  // that can be in the queue at any given time
  public IntStack(int maxSize) {
    ar = new int[maxSize];
  }

  // Returns the number of elements insize the stack
  public int size() {
    return pos;
  }

  // Returns true/false on whether the stack is empty
  public boolean isEmpty() {
    return pos == 0;
  }

  // Returns the element at the top of the stack
  @Override
  public Integer peek() {
    return ar[pos - 1];
  }

  // Add an element to the top of the stack
  @Override
  public void push(Integer value) {
    ar[pos++] = value;
  }

  // Make sure you check that the stack is not empty before calling pop!
  @Override
  public Integer pop() {
    return ar[--pos];
  }