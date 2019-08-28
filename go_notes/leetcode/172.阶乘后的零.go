/*
 * @lc app=leetcode.cn id=172 lang=golang
 *
 * [172] 阶乘后的零
 *
 * https://leetcode-cn.com/problems/factorial-trailing-zeroes/description/
 *
 * algorithms
 * Easy (39.20%)
 * Likes:    140
 * Dislikes: 0
 * Total Accepted:    15.5K
 * Total Submissions: 39.5K
 * Testcase Example:  '3'
 *
 * 给定一个整数 n，返回 n! 结果尾数中零的数量。
 * 
 * 示例 1:
 * 
 * 输入: 3
 * 输出: 0
 * 解释: 3! = 6, 尾数中没有零。
 * 
 * 示例 2:
 * 
 * 输入: 5
 * 输出: 1
 * 解释: 5! = 120, 尾数中有 1 个零.
 * 
 * 说明: 你算法的时间复杂度应为 O(log n) 。
 * 
 */
 func trailingZeroes(n int) int {
	// 只需要求出阶乘中有多少个5*2就可以了
	// 5 的数量是比2少的 所以直接计算出5的个数就是答案了
	var res int

	for n >= 5 {
		res += n/5
		n /= 5	
	}
	return res
}

