/*
 * @lc app=leetcode.cn id=206 lang=golang
 *
 * [206] 反转链表
 *
 * https://leetcode-cn.com/problems/reverse-linked-list/description/
 *
 * algorithms
 * Easy (63.33%)
 * Likes:    533
 * Dislikes: 0
 * Total Accepted:    84.5K
 * Total Submissions: 132.7K
 * Testcase Example:  '[1,2,3,4,5]'
 *
 * 反转一个单链表。
 * 
 * 示例:
 * 
 * 输入: 1->2->3->4->5->NULL
 * 输出: 5->4->3->2->1->NULL
 * 
 * 进阶:
 * 你可以迭代或递归地反转链表。你能否用两种方法解决这道题？
 * 
 */
/**
 * Definition for singly-linked list.
 * type ListNode struct {
 *     Val int
 *     Next *ListNode
 * }
 */
func reverseList(head *ListNode) *ListNode {
	var pre *ListNode
	
	var point = head

	for head != nil {
		// 记录现有节点的下一个节点
		point = head.Next
		// 将当前节点的下一个节点指向修改下的节点
		head.Next = pre
		// 修改下一个节点需要指向的节点
		pre = head
		// 将原有节点转移向下一个节点
		head = point
	}
	return pre
}

