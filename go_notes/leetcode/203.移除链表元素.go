/*
 * @lc app=leetcode.cn id=203 lang=golang
 *
 * [203] 移除链表元素
 *
 * https://leetcode-cn.com/problems/remove-linked-list-elements/description/
 *
 * algorithms
 * Easy (41.98%)
 * Likes:    271
 * Dislikes: 0
 * Total Accepted:    33K
 * Total Submissions: 78.5K
 * Testcase Example:  '[1,2,6,3,4,5,6]\n6'
 *
 * 删除链表中等于给定值 val 的所有节点。
 * 
 * 示例:
 * 
 * 输入: 1->2->6->3->4->5->6, val = 6
 * 输出: 1->2->3->4->5
 * 
 * 
 */
/**
 * Definition for singly-linked list.
 * type ListNode struct {
 *     Val int
 *     Next *ListNode
 * }
 */
func removeElements(head *ListNode, val int) *ListNode {
	if head == nil {
		return head
	}
	cur := head

	for cur.Next != nil {			// 从开头节点的下一个节点开始判断
		if cur.Next.Val == val {		// 下一个节点等于val 下一个个节点赋值为下一个节点的下一个节点
			cur.Next = cur.Next.Next
		} else {
			cur = cur.Next	// cur 后移
		}
	}
	if head.Val == val {  // 判断第一个节点
		return head.Next
	}

	return head
}

