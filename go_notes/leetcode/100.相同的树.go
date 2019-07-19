/*
 * @lc app=leetcode.cn id=100 lang=golang
 *
 * [100] 相同的树
 */
/**
 * Definition for a binary tree node.
 * type TreeNode struct {
 *     Val int
 *     Left *TreeNode
 *     Right *TreeNode
 * }
 */
func isSameTree(p *TreeNode, q *TreeNode) bool {
	return check(p,q)
}

func check(node1 *TreeNode,node2 *TreeNode) bool {
	if node1 == nil && node2 == nil {

		return true
	} else if node1 == nil || node2 == nil {

		return false
	}  else if node1.Val != node2.Val {

		return false
	} 
	return check(node1.Left,node2.Left) && check(node1.Right,node2.Right)
}

