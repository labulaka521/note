class BtreeNode:
    def __init__(self, label, parent):
        self.label = label
        self.left = None
        self.right = None
        self.parent = parent

    def getLabel(self):
        '获取根节点值'
        return self.label

    def setLabel(self, label):
        '设置根节点值'
        self.label = label

    def getLeft(self):
        '获取左分支'
        return self.left

    def getRight(self):
        '获取右分支'
        return self.right

    def setLeft(self, left):
        '''
        修改左子树
        
        param left: 需要修改的左子树
        type left: class BtreeNode
        '''
        self.left = left

    def setRight(self, right):
        '''
        修改右子树

        param right: 需要修改的右子树
        type right: class BtreeNode
        '''
        self.right = right
        
    def getParent(self):
        '获取父节点'
        return self.parent

    def setParent(self, parent):
        '''
        设置自已的父节点
        param parent: BtreeNode节点设置父亲节点
        type parent: class BtreeNode
        '''
        self.parent = parent

    def get_after(self):
        '获取自已的直接后继'
        right_child = self.getRight()
        
        while right_child.getLeft() is not None:
            right_child = right_child.getLeft()
        return right_child
        



# 前序遍历
## 递归版
def trav_pre(binnode):
    if not binnode:
        return None
    print(binnode.val)
    trav_pre(binnode.left)
    trav_pre(binnode.right)


##  迭代版1
def trav_pre_v1(binnode):
    '先遍历一个二叉树的左子树'           
    tmp_stack = []
    def  visitleftbranch(binnode_tree, tmp_stack):
        while binnode_tree:
            print(binnode_tree.val)
            if binnode_tree.right:
                tmp_stack.append(binnode_tree.right)
            binnode_tree = binnode_tree.left
    while True:
        visitleftbranch(binnode, tmp_stack)
        if len(tmp_stack) == 0:
            break
        binnode = tmp_stack.pop()


# 中序遍历
## 递归版
def trav_min(btree):
    '中序遍历递归版'
    if not btree:
        return btree
    trav_min(btree.left)
    print(btree.label, end=' ')
    trav_min(btree.right)


## 迭代版
def trav_min_v1(btree):
    '中序遍历迭代版'
    def golongbranch(btree_node, tmp_stack):
        while btree_node:
            tmp_stack.append(btree_node)
            btree_node = btree_node.left
    tmp_stack = []
    while True: 
        golongbranch(btree, tmp_stack)
        if len(tmp_stack) == 0:
            break
        btree = tmp_stack.pop()
        print(btree.val)
        btree = btree.right


def trav_end(btree):
    '后序遍历'
    s1 = [btree]
    s2 = []
    while len(s1) > 0:
        node = s1.pop()
        s2.append(node)
        if node.left:
            s1.append(node.left)
        if node.right:
            s1.append(node.right)
    while len(s2)>0:
        print(s2.pop().val, end=' ')


def trav_level(btree):
    from queue import Queue
    q = Queue()
    q.put(btree)
    while not q.empty():
        btree = q.get()
        print(btree.val)
        if btree.left: q.put(btree.left)
        if btree.right: q.put(btree.right)
        

# trav_pre(a)
# trav_pre_v1(a)

# trav_min(a)
# trav_min_v1(a)
# trav_level(a)
# trav_end(a)
