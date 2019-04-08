from bintree_ver2 import BtreeNode, trav_min


class BinarySearchtree:
    '''二叉搜索树的实现'''

    def __init__(self):
        self.root = None

    def is_empty(self):
        '二叉树是否为空'
        if self.root:
            return False
        return True

    def search(self, label):
        '''˜
        二叉搜索树查找

        param label: 查找的值
        type label: BtreeNode.label 节点的值
        '''
        curr_node = self.root
        if not self.is_empty():
            # 当前二叉树不为空且树根节点值不等于label查找的值
            while curr_node is not None and curr_node.getLabel() is not label:
                # 查找的值比树根节点的值小则取其左子树，否则取其右子树
                if label < curr_node.getLabel():
                    curr_node = curr_node.getLeft()
                else:
                    curr_node = curr_node.getRight()
        return curr_node

    def insert(self, label):
        '''
        二叉搜索树插入

        param label: 插入的值
        type label: BtreeNode.label 节点的值
        '''
        # 将插入元素写成一个二叉树节点
        new_node = BtreeNode(label, None)
        if self.is_empty():
            self.root = new_node
        else:
            curr_node = self.root
            # 寻找出插入目标节点
            while curr_node is not None:
                # 记录父节点
                parent_node = curr_node
                if new_node.getLabel() < curr_node.getLabel():
                    curr_node = curr_node.getLeft()
                else:
                    curr_node = curr_node.getRight()
            # 修改二叉树的左右子树
            if new_node.getLabel() < parent_node.getLabel():
                parent_node.setLeft(new_node)
            else:
                parent_node.setRight(new_node)
            # 修改新插入节点的父亲节点
            new_node.setParent(parent_node)

    def getMax(self):
        '''
        获取二叉搜索树最大的节点
        '''
        curr_node = self.root
        if not self.is_empty():
            # 循环直到二叉树的右子树为None
            while curr_node.getRight() is not None:
                curr_node = curr_node.getRight()
        return curr_node

    def getMin(self, root=None):
        '''
        获取二叉搜索树的最小节点
        '''
        curr_node = self.root
        # 节点不为空
        if not self.is_empty():
            # 循环 直到节点左子树为None
            while curr_node.getLeft() is not None:
                curr_node = curr_node.getLeft()
        return curr_node

    def delete(self, label):
        if not self.is_empty():
            del_node = self.search(label)
            # 当只有右子树时
            if del_node is None:
                return label
            # 只有右子树 先获取待删除树的父节点，然后确定带删除节点是父节点的左子树还是右子树，
            # 如果是左子树，就将父节点的左子树设置为待删除节点的右子树
            # 如果是右子树，就将父节点的右子树设置为待删除节点的右子树
            if not del_node.getLeft():
                # 获取自已的父节点
                del_parent = del_node.getParent()
                # 获取删除节点的右子树节点
                del_rchild = del_node.getRight()

                # 设置父节点的子节点 查看待删除节点是父节点的左还是右子树
                if del_parent.getLeft() == del_node:
                    del_parent.setLeft(del_rchild)
                else:
                    del_parent.setRight(del_rchild)

                # 设置删除节点右子树的父节点为删除节点的父节点
                if del_rchild is not None:
                    del_rchild.setParent(del_parent)
                return del_node.getLabel()

            # 只有左子树时 与上方相反
            elif not del_node.getRight():
                # 获取自已的父节点
                del_parent = del_node.getParent()
                # 获取删除节点的右子树节点
                del_lchild = del_node.getRight()

                # 代删除节点是父节点的左子树还是右子树
                if del_parent.get_Left() == del_node:
                    del_parent.setLeft(del_lchild)
                else:
                    del_parent.setRight(del_lchild)

                # 设置节点的父节点
                if del_lchild is not None:
                    del_lchild.setParent(del_parent)
                
                return del_node.getLabel()

            # 当左右子树都存在时 这时需要先找到待删除元素的后继，也就是待删除元素右子树的最小小节点
            # 然后与待删除节点替换后，然后这时就又成为了只有单个子树的情况
            else:
                # 通过self.getMin得到右子树的最小节点
                del_after = del_node.getRight().get_after()
                # 调换待删除节点和后继的值 此时则需要删除待删除节点的后继即可
                del_node.label, del_after.label = del_after.label, del_node.label

                # 获取删除节点后继的父节点
                del_after_parent = del_after.getParent()
                # 这时del_after只有右子树或者没有
                del_after_rchild = del_after.getRight()

                # 设置父节点的左子树，因为只有左子树
                del_after_parent.setLeft(del_after_rchild)

                # 设置del_after_rchild的父节点为del_after_parent
                if del_after_rchild is not None:
                    del_after_rchild.setParent(del_after_parent)



def testBinSearchtree():
    '''
    Example
                  8
                 / \
                3   10
               / \    \
              1   6    14
                 / \   /
                4   7 13 
    '''

    '''
    Example After Deletion
                  7
                 / \
                1   4
    '''
    bt = BinarySearchtree()
    bt.insert(8)
    bt.insert(3)
    bt.insert(6)
    bt.insert(1)
    bt.insert(10)
    bt.insert(14)
    bt.insert(13)
    bt.insert(4)
    bt.insert(7)
    bt.delete(8)
    trav_min(bt.root)

    # print(bt.root.get_after())
    # # trav_min(bt.root)


testBinSearchtree()
