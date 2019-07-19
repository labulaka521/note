/*
 * @lc app=leetcode.cn id=107 lang=golang
 *
 * [107] 二叉树的层次遍历 II
 *
 * https://leetcode-cn.com/problems/binary-tree-level-order-traversal-ii/description/
 *
 * algorithms
 * Easy (61.46%)
 * Likes:    116
 * Dislikes: 0
 * Total Accepted:    19.5K
 * Total Submissions: 31.8K
 * Testcase Example:  '[3,9,20,null,null,15,7]'
 *
 * 给定一个二叉树，返回其节点值自底向上的层次遍历。 （即按从叶子节点所在层到根节点所在的层，逐层从左向右遍历）
 * 
 * 例如：
 * 给定二叉树 [3,9,20,null,null,15,7],
 * 
 * ⁠   3
 * ⁠  / \
 * ⁠ 9  20
 * ⁠   /  \
 * ⁠  15   7
 * 
 * 
 * 返回其自底向上的层次遍历为：
 * 
 * [
 * ⁠ [15,7],
 * ⁠ [9,20],
 * ⁠ [3]
 * ]
 * 
 * 
 */
/**
 * Definition for a binary tree node.
 * type TreeNode struct {
 *     Val int
 *     Left *TreeNode
 *     Right *TreeNode
 * }
 */
func levelOrderBottom(root *TreeNode) [][]int {
	// 先将根节点存储，然后循环，记录这个节点的值，然后将这个节点的左右子节点添加,

	res := make([][]int,0)
	if root == nil {									// 为nil直接返回
		return res										
	}
	nodes := make([]*TreeNode,0)
	nodes = append(nodes,root)
	for len(nodes)!=0 {									// nodes不为0就一直循环
		tmp := []int{}									// 记录这层的数值
		count := len(nodes)								// 统计这一层的节点数
		for i :=0;i<count;i++ { 						// 循环次数等于每一层的节点数，每次都取第一个node，因为下面会将第一个node删除
			tmp = append(tmp,nodes[0].Val)				// 记录节点值
			if nodes[0].Left != nil {					// 如果左子树不为空，将左子树添加nodes
				nodes = append(nodes,nodes[0].Left)
			}
			if nodes[0].Right != nil {					// 如果右子树不为空，将右子树添加到nodes
				nodes = append(nodes,nodes[0].Right)
			}
			nodes = nodes[1:]							// 将第一个node删除
		}
		res = append(res,tmp)							// 记录每一层的值
	}
	i,j := 0,len(res)-1
	for i<j  {											// 反转每一层的值
		tmp := res[i]
		res[i] = res[j]
		res[j] = tmp
		i ++
		j --
	}
	return res											// 返回结果
}

