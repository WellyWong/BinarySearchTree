#Reference: clrs chapter 12

class Node:
    def __init__(self, val):
        self.value = val
        self.left = None
        self.right = None
        self.parent = None

    def __repr__(self):
        return str(self.value)

class Tree:
    def __init__(self):
        self.root = None

    def get_root(self):
        return self.root

    def add(self, key):
        if self.root == None:
            self.root = Node(key)
            return
        curr = self.root
        while curr:
            if key < curr.value:
                if curr.left == None:
                    curr.left = Node(key)
                    curr.left.parent = curr
                    return
                else:
                    curr = curr.left
            elif key > curr.value:
                if curr.right == None:
                    curr.right = Node(key)
                    curr.right.parent = curr
                    return
                else:
                    curr = curr.right
            elif key == curr.value:
                print("Key already exist in the tree")
                return

    def insert(self, key):    #from clrs 12.3
        z = Node(key)
        y = None        #this y will serve as a pointer to previous node (parent of x), x pointer will find position to insert
        x = self.root
        while x != None:
            y = x
            if z.value < x.value:
                x = x.left
            else:
                x = x.right
        z.parent = y
        if y == None:       #empty tree, make z a root node
            self.root = z
        elif z.value < y.value:
            y.left = z
        else:
            y.right = z
    #Note: Equal keys pose a problem for the implementation of binary search trees. (page 303-304, clrs)
    #https://www.geeksforgeeks.org/how-to-handle-duplicates-in-binary-search-tree/

    def inorder(self, root):
        if root != None:
            self.inorder(root.left)
            print(root.value, end=' ')
            self.inorder(root.right)

    def preorder(self, root):
        if root != None:
            print(root.value, end=' ')
            self.preorder(root.left)
            self.preorder(root.right)

    def postorder(self, root):
        if root != None:
            self.postorder(root.left)
            self.postorder(root.right)
            print(root.value, end=' ')

    def print(self, order):
        if order == 'inorder':
            self.inorder(self.root)
        elif order == 'preorder':
            self.preorder(self.root)
        else:
            self.postorder(self.root)
        print("\n")

    def find(self, key):
        if self.root == None:
            return None
        else:
            return self.find_helper(key, self.root)

    def find_helper(self, key, node):
        if node == None or node.value == key:
            return node
        if key < node.value:
            return self.find_helper(key, node.left)
        else:   #key > root.value:
            return self.find_helper(key, node.right)

    def find_iterative(self, key):
        return self.find_iterative_helper(key, self.root)

    def find_iterative_helper(self, key, root):
        while root != None and root.value != key:
            if key < root.value:
                root = root.left
            else:
                root = root.right
        return root

    def min(self, node):
        while node.left != None:
            node = node.left
        return node

    def max(self, node):
        while node.right != None:
            node = node.right
        return node

    #Given a node in a binary search tree, sometimes we need to find its successor in the sorted order determined
    # by an inorder tree walk. If all keys are distinct, the successor of a node x
    # is the node with the smallest key greater than x.key
    # The structure of a binary search tree allows us to determine the successor of a node without ever comparing keys.
    # The following procedure returns the successor of a node x in a binary search tree if it exists,
    # and NIL if x has the largest key in the tree:
    def successor(self, x):
        if x.right != None:
            return self.min(x.right)
        y = x.parent
        while y != None and x == y.right:
            x = y
            y = y.parent
        return y

    def predecessor(self, x):
        if x.left != None:
            return self.max(x.left)
        y = x.parent
        while y != None and x == y.left:
            x = y
            y = y.parent
        return y

    #TRANSPLANT replaces the subtree rooted at node u with the subtree rooted at node v,
    #node u’s parent becomes node v’s parent, and u’s parent ends up having v as its appropriate child.
    def transplant(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v is not None:   #since we allow v to be None, we have to check this condition
            v.parent = u.parent
    #Note that TRANSPLANT does not attempt to update v.left and v.right; doing so or not doing so,
    # is the responsibility of TRANSPLANT’s caller.

    def delete_helper(self, z):    #z is the node to be deleted
        if z.left == None:
            self.transplant(z, z.right)
        elif z.right == None:
            self.transplant(z, z.left)
        else:
            y = self.min(z.right)   #refer to figure 12.4 clrs (page 297)
            if y.parent != z:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self.transplant(z, y)
            y.left = z.left
            y.left.parent = y

    def delete(self, key):
        z = self.find(key)
        self.delete_helper(z)

    #Depth of a node = number of edges in the path from root to that node
    #Height of a node = number of edges in the longest path from that node to a leaf node
    #Height of a tree = height of the root, or max depth of any node in the tree
    def height(self, node):
        if node is None:
            return -1       #this will make the leaf node height = 0
        else:
            l_height = self.height(node.left)
            r_height = self.height(node.right)

            return max(l_height, r_height) + 1
       
    def print_vertical(self):
        stack = []
        margin_stack = []
        stack.append(self.root)
        margin_stack.append((0, '_'))
        while len(stack) > 0:
            node = stack.pop()
            margin, l_or_r_child = margin_stack.pop()
            for i in range(margin):
                print("     ", end='')
            if margin > 0:
                print(l_or_r_child + "---", end='')
            else:
                print('Root:', end='')

            if node != None:
                if node.left != None or node.right != None:
                    stack.append(node.right)
                    margin_stack.append((margin+1, 'R'))
                    stack.append(node.left)
                    margin_stack.append((margin+1, 'L'))
                print(node)
            else:
                print("[]")


def inorder_iterative(root):
    stack = []
    curr = root
    done = 0
    while not done:
        if curr:
            stack.append(curr)
            curr = curr.left
        else:
            if len(stack) > 0:
                curr = stack.pop()
                print(curr.value, end=' ')
                curr = curr.right
            else:
                done = 1

#      3
#   1     4
# 0   2     8
tree = Tree()
tree.insert(3)
tree.insert(1)
tree.insert(4)
tree.insert(0)
tree.insert(8)
tree.insert(2)
tree.print_vertical()
"""
Output:
Root:3
     L---1
          L---0
          R---2
     R---4
          L---[]
          R---8
"""
