/*
 * @lc app=leetcode.cn id=136 lang=golang
 *
 * [136] 只出现一次的数字
 *
 * https://leetcode-cn.com/problems/single-number/description/
 *
 * algorithms
 * Easy (62.51%)
 * Likes:    779
 * Dislikes: 0
 * Total Accepted:    85.4K
 * Total Submissions: 136.7K
 * Testcase Example:  '[2,2,1]'
 *
 * 给定一个非空整数数组，除了某个元素只出现一次以外，其余每个元素均出现两次。找出那个只出现了一次的元素。
 * 
 * 说明：
 * 
 * 你的算法应该具有线性时间复杂度。 你可以不使用额外空间来实现吗？
 * 
 * 示例 1:
 * 
 * 输入: [2,2,1]
 * 输出: 1
 * 
 * 
 * 示例 2:
 * 
 * 输入: [4,1,2,1,2]
 * 输出: 4
 * 
 */
func singleNumber(nums []int) int {
	// 借助map
	// 使用了额外的空间
	// store := map[int]int{}
    // for _, n := range nums {
	// 	v:= store[n]
	// 	store[n] = v + 1
	// }
	// for k,v:=range store {
	// 	if v == 1 {
	// 		return k
	// 	}
	// }
	// return 0

	// 使用异或 XOR
	// 对一个值使用两次异或后值是不变的
	var c int

	for _, n:= range nums {
		c ^= n
	}
	return c
}

