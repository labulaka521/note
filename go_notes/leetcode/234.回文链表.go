/*
 * @lc app=leetcode.cn id=234 lang=golang
 *
 * [234] 回文链表
 *
 * https://leetcode-cn.com/problems/palindrome-linked-list/description/
 *
 * algorithms
 * Easy (38.18%)
 * Likes:    256
 * Dislikes: 0
 * Total Accepted:    34K
 * Total Submissions: 88.7K
 * Testcase Example:  '[1,2]'
 *
 * 请判断一个链表是否为回文链表。
 * 
 * 示例 1:
 * 
 * 输入: 1->2
 * 输出: false
 * 
 * 示例 2:
 * 
 * 输入: 1->2->2->1
 * 输出: true
 * 
 * 
 * 进阶：
 * 你能否用 O(n) 时间复杂度和 O(1) 空间复杂度解决此题？
 * 
 */
/**
 * Definition for singly-linked list.
 * type ListNode struct {
 *     Val int
 *     Next *ListNode
 * }
 */
func isPalindrome(head *ListNode) bool {
	// TODO 快慢指针
	if head == nil || head.Next == nil {
		return true
	}
	// 反转节点然后匹配
	var countnode int
	sum := head
	for sum != nil {
		countnode ++
		sum = sum.Next	
	}

	// 是偶数个节点吗
	ou := countnode % 2 == 0

	// 反转前半段链表
	var reversenode *ListNode
	var tmp = head
	for i := 0; i<countnode/2;i++ {
		next := tmp.Next         	// 记录下一个节点
		tmp.Next = reversenode		// 将当前节点的下一个节点指向反转的节点 前一个节点
		reversenode = tmp			// 将已反转的节点指向当前节点
		tmp = next					// 将当前的节点指向下一个已经记录的节点
	}	
	
	// 如果是奇数就将剩下的右半段链表右移动以为
	if !ou {
		tmp = tmp.Next
	}
	// 计算反转后的前半段链表的值和后半段未反转是否相等
	for tmp != nil {
		if tmp.Val != reversenode.Val {
			return false
		}
		tmp = tmp.Next
		reversenode = reversenode.Next
	}
	
	return true

}

