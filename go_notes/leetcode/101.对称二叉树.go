/*
 * @lc app=leetcode.cn id=101 lang=golang
 *
 * [101] 对称二叉树
 */
/**
 * Definition for a binary tree node.
 * type TreeNode struct {
 *     Val int
 *     Left *TreeNode
 *     Right *TreeNode
 * }
 */
func isSymmetric(root *TreeNode) bool {
	// 使用迭代比较对应的节点
   return isMirror(root,root)
}
func isMirror(t1 *TreeNode,t2 *TreeNode) bool {
	// 都为nil返回true
	if t1 == nil && t2 == nil {
		return true
	}
	// 表明已经不相等
	if t1 == nil || t2 == nil {
		return false
	}
	// 比较对应的节点值
	if t1.Val != t2.Val {
		return false
	}
	return isMirror(t1.Left,t2.Right) && isMirror(t1.Right,t2.Left)
}

