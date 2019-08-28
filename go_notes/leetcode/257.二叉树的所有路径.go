/*
 * @lc app=leetcode.cn id=257 lang=golang
 *
 * [257] 二叉树的所有路径
 *
 * https://leetcode-cn.com/problems/binary-tree-paths/description/
 *
 * algorithms
 * Easy (59.32%)
 * Likes:    146
 * Dislikes: 0
 * Total Accepted:    13.7K
 * Total Submissions: 22.9K
 * Testcase Example:  '[1,2,3,null,5]'
 *
 * 给定一个二叉树，返回所有从根节点到叶子节点的路径。
 * 
 * 说明: 叶子节点是指没有子节点的节点。
 * 
 * 示例:
 * 
 * 输入:
 * 
 * ⁠  1
 * ⁠/   \
 * 2     3
 * ⁠\
 * ⁠ 5
 * 
 * 输出: ["1->2->5", "1->3"]
 * 
 * 解释: 所有根节点到叶子节点的路径为: 1->2->5, 1->3
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
func binaryTreePaths(root *TreeNode) []string {
	// 深度遍历
	paths := make([]string,0,10000)
	collect_path(root,"",&paths)
	return paths
	
}


func collect_path(node *TreeNode,path string, paths *[]string) {
	if node == nil {
		return
	}

	if path == "" {
		path += fmt.Sprintf("%d",node.Val)
	} else {
		path += fmt.Sprintf("->%d",node.Val)
	}
	if node.Left == nil && node.Right == nil {
		*paths = append(*paths, path)
		return
	}
	collect_path(node.Left,path,paths)
	collect_path(node.Right,path,paths)
}
