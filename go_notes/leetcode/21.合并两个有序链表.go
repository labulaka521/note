/*
 * @lc app=leetcode.cn id=21 lang=golang
 *
 * [21] 合并两个有序链表
 */
/**
 * Definition for singly-linked list.
 * type ListNode struct {
 *     Val int
 *     Next *ListNode
 * }
 */
func mergeTwoLists(l1 *ListNode, l2 *ListNode) *ListNode {
	res := &ListNode{}
	cur := res
	for l1 != nil && l2 != nil {
		if l1.Val > l2.Val {
			cur.Next = l2	
			cur = cur.Next  // 转向新添加的节点
			l2 = l2.Next  // 转向l2下一个节点
		} else {
			cur.Next = l1
			cur = cur.Next
			l1 = l1.Next
		}
	}
	if l1 != nil {
		cur.Next = l1 // 进入这里的时候l2已经为nil
	}

	if l2 != nil {
		cur.Next = l2 // 进入这里的时候l1已经为nil
	}
	return res.Next
}

