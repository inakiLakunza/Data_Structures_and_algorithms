

public class SplayTree<T extends Comparable<T>> {

  private BinaryTree<T> root;

  public static class BinaryTree<T extends Comparable<T>> implements TreePrinter.PrintableNode {
    private T data;
    private BinaryTree<T> leftChild, rightChild;

    public BinaryTree(T data) {
      if (data == null) {
        try {
          throw new Exception("Null data not allowed into tree");
        } catch (Exception e) {
          e.printStackTrace();
        }
      } else this.data = data;
    }

    @Override
    public BinaryTree<T> getLeft() {
      return leftChild;
    }

    public void setLeft(BinaryTree<T> leftChild) {
      this.leftChild = leftChild;
    }

    @Override
    public BinaryTree<T> getRight() {
      return rightChild;
    }

    public void setRight(BinaryTree<T> rightChild) {
      this.rightChild = rightChild;
    }

    @Override
    public String getText() {
      return data.toString();
    }

    public T getData() {
      return data;
    }

    public void setData(T data) {
      if (data == null) {
        try {
          throw new Exception("Null data not allowed into tree");
        } catch (Exception e) {
          e.printStackTrace();
        }
      } else this.data = data;
    }

    @Override
    public String toString() {

      return TreePrinter.getTreeDisplay(this);
    }
  }

  /** Public Methods * */
  public SplayTree() {
    this.root = null;
  }

  public SplayTree(BinaryTree<T> root) {
    this.root = root;
  }

  public BinaryTree<T> getRoot() {
    return root;
  }

  /** Searches a node and splays it on top,returns the new root * */
  public BinaryTree<T> search(T node) {
    if (root == null) return null;

    this.root = splayUtil(root, node);

    return this.root.getData().compareTo(node) == 0 ? this.root : null;
  }

  /** Inserts a node into the tree and splays it on top, returns the new root* */
  public BinaryTree<T> insert(T node) {
    if (root == null) {
      root = new BinaryTree<>(node);
      return root;
    }
    splay(node);

    ArrayList<BinaryTree<T>> l_r = split(node);

    BinaryTree<T> left = l_r.get(0);
    BinaryTree<T> right = l_r.get(1);

    root = new BinaryTree<>(node);
    root.setLeft(left);
    root.setRight(right);

    return root;
  }

  /** Deletes a node,returns the new root * */
  public BinaryTree<T> delete(T node) {
    if (root == null) return null;

    BinaryTree<T> searchResult = splay(node);

    if (searchResult.getData().compareTo(node) != 0) return null;

    BinaryTree<T> leftSubtree = root.getLeft();
    BinaryTree<T> rightSubtree = root.getRight();

    // Set the 'to be deleted' key ready for garbage collection
    root.setLeft(null);
    root.setRight(null);

    root = join(leftSubtree, rightSubtree);

    return root;
  }

  /** To FindMax Of Entire Tree * */
  public T findMax() {
    BinaryTree<T> temp = root;
    while (temp.getRight() != null) temp = temp.getRight();
    return temp.getData();
  }

  /** To FindMin Of Entire Tree * */
  public T findMin() {
    BinaryTree<T> temp = root;
    while (temp.getLeft() != null) temp = temp.getLeft();
    return temp.getData();
  }

  /** * To FindMax Of Tree with specified root * */
  public T findMax(BinaryTree<T> root) {
    BinaryTree<T> temp = root;
    while (temp.getRight() != null) temp = temp.getRight();
    return temp.getData();
  }

  /** * To FindMin Of Tree with specified root * */
  public T findMin(BinaryTree<T> root) {
    BinaryTree<T> temp = root;
    while (temp.getLeft() != null) temp = temp.getLeft();
    return temp.getData();
  }

  @Override
  public String toString() {

    System.out.println("Elements:" + inorder(root, new ArrayList<>()));
    return (root != null) ? root.toString() : null;
  }

  /** Private Methods * */
  private BinaryTree<T> rightRotate(BinaryTree<T> node) {
    BinaryTree<T> p = node.getLeft();
    node.setLeft(p.getRight());
    p.setRight(node);
    return p;
  }

  private BinaryTree<T> leftRotate(BinaryTree<T> node) {
    BinaryTree<T> p = node.getRight();
    node.setRight(p.getLeft());
    p.setLeft(node);
    return p;
  }

  private BinaryTree<T> splayUtil(BinaryTree<T> root, T key) {
    if (root == null || root.getData() == key) return root;

    if (root.getData().compareTo(key) > 0) {
      if (root.getLeft() == null) return root;

      if (root.getLeft().getData().compareTo(key) > 0) {

        root.getLeft().setLeft(splayUtil(root.getLeft().getLeft(), key));

        root = rightRotate(root);
      } else if (root.getLeft().getData().compareTo(key) < 0) {

        root.getLeft().setRight(splayUtil(root.getLeft().getRight(), key));

        if (root.getLeft().getRight() != null) root.setLeft(leftRotate(root.getLeft()));
      }
      return (root.getLeft() == null) ? root : rightRotate(root);
    } else {
      if (root.getRight() == null) return root;

      if (root.getRight().getData().compareTo(key) > 0) {
        root.getRight().setLeft(splayUtil(root.getRight().getLeft(), key));
        if (root.getRight().getLeft() != null) root.setRight(rightRotate(root.getRight()));
      } else if (root.getRight().getData().compareTo(key) < 0) // Zag-Zag (Right Right)
      {
        root.getRight().setRight(splayUtil(root.getRight().getRight(), key));
        root = leftRotate(root);
      }

      return (root.getRight() == null) ? root : leftRotate(root);
    }
  }

  private BinaryTree<T> splay(T node) {
    if (root == null) return null;

    this.root = splayUtil(root, node);

    return this.root;
  }

  private ArrayList<BinaryTree<T>> split(T node) {
    BinaryTree<T> right;
    BinaryTree<T> left;

    if (node.compareTo(root.getData()) > 0) {
      right = root.getRight();
      left = root;
      left.setRight(null);
    } else {
      left = root.getLeft();
      right = root;
      right.setLeft(null);
    }
    ArrayList<BinaryTree<T>> l_r = new ArrayList<>();
    l_r.add(left);
    l_r.add(right);

    return l_r;
  }

  private BinaryTree<T> join(BinaryTree<T> L, BinaryTree<T> R) {

    if (L == null) {
      root = R;
      return R;
    }
    root = splayUtil(L, findMax(L));
    root.setRight(R);
    return root;
  }

  private ArrayList<T> inorder(BinaryTree<T> root, ArrayList<T> sorted) {

    if (root == null) {
      return sorted;
    }
    inorder(root.getLeft(), sorted);
    sorted.add(root.getData());
    inorder(root.getRight(), sorted);
    return sorted;
  }
}