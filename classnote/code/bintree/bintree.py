class BTree:
    '''
    使用列表实现二叉树
    主要的接口:
        BTree:
            初始化一个二叉树
        is_empty: 
            判断一个二叉树是否为空
        data: 
            返回二叉树的树根节点数据
        left: 
            返回二叉树的左子树
        right: 
            返回二叉树的右子树
        set_root: 
            修改二叉树的根节点
        set_left:
            修改二叉树的左子树
        set_right:
            修改二叉树的右子数
    '''

    def __init__(self, data=None, left=None, right=None):
        '''
        二叉树的node实现
        args: int()
            bintree1
            bintree2
        return: bintree type-> list

        btree = BTree(1,Btree(2), Btree(3))
        '''
        self.btree = [data, left, right]

    def is_empty(self):
        '''
        判断二叉树是否为空
        args: btree
        return: True / False type->boolen
        '''
        return self.root is None

    def root(self):
        '''
        返回树根节点
        args: btree
        return: btree_root_data type->int
        '''
        return self.btree[0]

    def left(self):
        '''
        返回二叉树的左子树
        args: bintree
        return: bintree_left  type-> list
        '''
        return self.btree[1]

    def right(self):
        '''
        返回二叉树的右子树
        args: bintree
        return: bintree_right type -> list
        '''
        return self.btree[2]

    def set_root(self, data):
        '''
        修改二叉树的的根结点
        args: btree
            data
        return:
        '''
        self.btree[0] = data

    def set_left(self, left):
        '''
        修改二叉树的左子数
        args: btree
              left 二叉树
        return: 
        '''
        self.btree[1] = left

    def set_right(self, right):
        '''
        修改二叉树的右子树
        args: btree
              right 二叉树
        return:
        '''
        self.btree[2] = right


# 递归版本
def trav_pre_1(btree):
    '''先序遍历'''
    if not btree:
        return
    print(btree.root(),end=' ')
    trav_pre_1(btree.left())
    trav_pre_1(btree.right())

def trav_mid_1(btree):
    '''中序遍历'''
    if not btree:
        return
    trav_mid_1(btree.left())
    print(btree.root(), end=' ')
    trav_mid_1(btree.right())

def trav_after_1(btree):
    '''后序遍历'''
    if not btree:
        return
    trav_after_1(btree.left())
    trav_after_1(btree.right())
    print(btree.root())




# 迭代版本
def trav_pre(btree):
    '''
    先序遍历
    args: btree
    return list 二叉树的中序遍历列表
    '''
    visit = list()

    def VisitAlongLeftBranch(x, tmp_stack):
        '''遍历二叉树的左子树节点'''
        while x:
            visit.append(x.root())              # 访问元素
            if x.right():                       # 如果右侧子树存在则将入栈
                tmp_stack.append(x.right())
            x = x.left()                        # 转向当前节点的左子树

    tmp_stack = list()
    while True:
        VisitAlongLeftBranch(btree, tmp_stack)  # 遍历当前节点的所有左子树
        if len(tmp_stack) == 0:                 # 如果临时栈为空则为已处理完所有节点退出程序
            break
        btree = tmp_stack.pop()                 # 弹出临时栈的上一个节点
    print(visit)

def trav_mid(btree):
    '''
    中序遍历
    return list
    '''
    visit = list()                              # 存放遍历列表
    tmp_stack = list()                          #辅助栈
    def golongleftbranch(tmp_stack, btree):
        # 遍历左侧分枝并依次入栈
        while btree:                            # 当二叉树不为空的时候
            tmp_stack.append(btree)             # 入栈
            btree = btree.left()                # 转向二叉树左节点
    while True:
        golongleftbranch(tmp_stack, btree)      # 依次进站
        if len(tmp_stack) == 0:                 # 临时栈为空已经处理完
            break
        btree = tmp_stack.pop()                 # 获取临时栈中栈顶元素
        visit.append(btree.root())              # 访问二叉树根节点
        btree = btree.right()                   # 转向二叉树的右节点
    print(visit)


def trav_after(btree):
    '''
    后序遍历
    '''
    visit = list()
    def gotoHLVEF(btree):
        while btree == stack[0]:
            if btree.left():
                if btree.right():
                    stack.append(btree.right())
                stack.append(btree.right())
            else:
                stack.append(btree.right())
        # print(sta)
    stack = []
    if btree:stack.append(btree)
    while len(stack) != 0:
        gotoHLVEF(btree)
        btree = stack.pop()
        visit.append(btree.root())




def trav_level(btree):
    '''
    层次访问
    '''
    visit = list()
    from queue import Queue
    q = Queue()
    q.put(btree)                                # 将根节点放入队列
    while not q.empty():                        # 队列不为空
        btree = q.get()                         # 队列中取出元素
        visit.append(btree.root())              # 访问元素
        if btree.left():q.put(btree.left())     # 将左节点放入队列
        if btree.right():q.put(btree.right())   # 将右节点放入队列
    print(visit)












    

a = BTree(1, BTree(2), BTree(3))
b = BTree(9,a,a)
# trav_pre_1(b)
# print('')
# trav_mid_1(b)
# trav_after_1(a)
# trav_pre(b)
# trav_mid(b)
# trav_level(b)
trav_after(a)
