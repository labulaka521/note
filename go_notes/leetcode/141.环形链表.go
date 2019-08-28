/*
 * @lc app=leetcode.cn id=141 lang=golang
 *
 * [141] 环形链表
 *
 * https://leetcode-cn.com/problems/linked-list-cycle/description/
 *
 * algorithms
 * Easy (41.73%)
 * Likes:    337
 * Dislikes: 0
 * Total Accepted:    54K
 * Total Submissions: 129.3K
 * Testcase Example:  '[3,2,0,-4]\n1'
 *
 * 给定一个链表，判断链表中是否有环。
 * 
 * 为了表示给定链表中的环，我们使用整数 pos 来表示链表尾连接到链表中的位置（索引从 0 开始）。 如果 pos 是 -1，则在该链表中没有环。
 * 
 * 
 * 
 * 示例 1：
 * 
 * 输入：head = [3,2,0,-4], pos = 1
 * 输出：true
 * 解释：链表中有一个环，其尾部连接到第二个节点。
 * 
 * 
 * 
 * 
 * 示例 2：
 * 
 * 输入：head = [1,2], pos = 0
 * 输出：true
 * 解释：链表中有一个环，其尾部连接到第一个节点。
 * 
 * 
 * 
 * 
 * 示例 3：
 * 
 * 输入：head = [1], pos = -1
 * 输出：false
 * 解释：链表中没有环。
 * 
 * 
 * 
 * 
 * 
 * 
 * 进阶：
 * 
 * 你能用 O(1)（即，常量）内存解决此问题吗？
 * 
 */
/**
 * Definition for singly-linked list.
 * type ListNode struct {
 *     Val int
 *     Next *ListNode
 * }
 */
func hasCycle(head *ListNode) bool {
	// 使用map 将走过的点记录下来，然后每次走的时候判断是否已经走过了 如果走过就是唤醒列表

	// 使用两个	快慢指针来进行
	// 快指针每次走两步，慢指针每次走一步，
	// 如果不是环形列表，则到最后等值为nil的时候退出返回false
	// 如果是环形链表，那么快指针一定会在某个时间点再次追赶上慢指针
	if head == nil {
		return false
	}
	var slow = head
	var quick = head.Next

	for slow != quick {
		if quick ==nil || quick.Next == nil {
			return false
		}
		slow = slow.Next
		quick = quick.Next.Next
	}
	return true
}

