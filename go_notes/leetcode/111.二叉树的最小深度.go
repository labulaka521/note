/*
 * @lc app=leetcode.cn id=111 lang=golang
 *
 * [111] 二叉树的最小深度
 *
 * https://leetcode-cn.com/problems/minimum-depth-of-binary-tree/description/
 *
 * algorithms
 * Easy (39.31%)
 * Likes:    138
 * Dislikes: 0
 * Total Accepted:    23.4K
 * Total Submissions: 59.3K
 * Testcase Example:  '[3,9,20,null,null,15,7]'
 *
 * 给定一个二叉树，找出其最小深度。
 * 
 * 最小深度是从根节点到最近叶子节点的最短路径上的节点数量。
 * 
 * 说明: 叶子节点是指没有子节点的节点。
 * 
 * 示例:
 * 
 * 给定二叉树 [3,9,20,null,null,15,7],
 * 
 * ⁠   3
 * ⁠  / \
 * ⁠ 9  20
 * ⁠   /  \
 * ⁠  15   7
 * 
 * 返回它的最小深度  2.
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
func minDepth(root *TreeNode) int {
	// 叶子节点的定义式左右子树都为空的时叫做叶子节点
	// 当root左右孩子为空时返回1
	// 当root节点孩子是有一个为空时，返回不为空的孩子的节点深度
	// 当root节点左右孩子都不为空的情况下，返回左右孩子较小深度的节点值
    if root == nil {
		return 0
	}
	if root.Left == nil && root.Right == nil {
		return 1
	}
	lh := minDepth(root.Left)
	rh := minDepth(root.Right)
	if root.Left == nil || root.Right == nil {
		return lh + rh + 1
	}
	min := lh
	if lh > rh {
		min = rh
	}
	return min + 1
}


