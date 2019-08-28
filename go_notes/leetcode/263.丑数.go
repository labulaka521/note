/*
 * @lc app=leetcode.cn id=263 lang=golang
 *
 * [263] 丑数
 *
 * https://leetcode-cn.com/problems/ugly-number/description/
 *
 * algorithms
 * Easy (47.06%)
 * Likes:    68
 * Dislikes: 0
 * Total Accepted:    14.1K
 * Total Submissions: 29.7K
 * Testcase Example:  '6'
 *
 * 编写一个程序判断给定的数是否为丑数。
 * 
 * 丑数就是只包含质因数 2, 3, 5 的正整数。
 * 
 * 示例 1:
 * 
 * 输入: 6
 * 输出: true
 * 解释: 6 = 2 × 3
 * 
 * 示例 2:
 * 
 * 输入: 8
 * 输出: true
 * 解释: 8 = 2 × 2 × 2
 * 
 * 
 * 示例 3:
 * 
 * 输入: 14
 * 输出: false 
 * 解释: 14 不是丑数，因为它包含了另外一个质因数 7。
 * 
 * 说明：
 * 
 * 
 * 1 是丑数。
 * 输入不会超过 32 位有符号整数的范围: [−2^31,  2^31 − 1]。
 * 
 * 
 */
func isUgly(num int) bool {
	// 先判断是否除以次数的余数是否为0
	// 然后如果为0 就是
	if num <=0 {
		return false
	}

	chuyi :=[]int{2,3,5}
	for num > 1 {
		var exist bool

		for _, i := range chuyi {
			if num % i == 0 {
				exist = true
				num = num / i
				break
			}
		}
		if !exist {
			return false
		}
	}
	if num == 1 {
		return true
	}
	return false
}

