/*
 * @lc app=leetcode.cn id=83 lang=golang
 *
 * [83] 删除排序链表中的重复元素
 */
/**
 * Definition for singly-linked list.
 * type ListNode struct {
 *     Val int
 *     Next *ListNode
 * }
 */
func deleteDuplicates(head *ListNode) *ListNode {
	if head == nil {
		return head
	}
	dummyHead := head
	// 判断不为nil
	for head.Next != nil {
		// 相等 修改
		if head.Val == head.Next.Val {
			head.Next = head.Next.Next
			continue
		}
		// 不想等转移到下一节点
		head = head.Next
	}

	return dummyHead

}

