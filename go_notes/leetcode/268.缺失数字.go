/*
 * @lc app=leetcode.cn id=268 lang=golang
 *
 * [268] 缺失数字
 *
 * https://leetcode-cn.com/problems/missing-number/description/
 *
 * algorithms
 * Easy (51.74%)
 * Likes:    157
 * Dislikes: 0
 * Total Accepted:    29.6K
 * Total Submissions: 56.6K
 * Testcase Example:  '[3,0,1]'
 *
 * 给定一个包含 0, 1, 2, ..., n 中 n 个数的序列，找出 0 .. n 中没有出现在序列中的那个数。
 * 
 * 示例 1:
 * 
 * 输入: [3,0,1]
 * 输出: 2
 * 
 * 
 * 示例 2:
 * 
 * 输入: [9,6,4,2,3,5,7,0,1]
 * 输出: 8
 * 
 * 
 * 说明:
 * 你的算法应具有线性时间复杂度。你能否仅使用额外常数空间来实现?
 * 
 */
func missingNumber(nums []int) int {
	// if len(nums) == 0 {
	// 	return 0
	// }
	// if len(nums) == 1 && nums[0] == 0 {
	// 	return 1
	// }
	// if len(nums) == 1 && nums[0] == 1 {
	// 	return 0
	// }
	// var max = nums[0]
	// var min = nums[0]
	var count int

	// for _, i := range nums {
	// 	if i < min {   							// 寻找最小的数
	// 		min = i
	// 	}
	// 	if i > max {							// 寻找最大的数
	// 		max = i
	// 	}
	// 	count += i
	// }
	// if min != 0 {
	// 	return 0
	// }
	// if max - min == len(nums) - 1 {
	// 	return max + 1
	// }
	// realcount := (len(nums) + 1 ) * (min + max) / 2


	realcount := len(nums) * (len(nums) + 1) / 2
	for _,i := range nums {
		count += i
	}
	return realcount - count

}

