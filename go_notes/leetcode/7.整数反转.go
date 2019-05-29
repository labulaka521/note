/*
 * @lc app=leetcode.cn id=7 lang=golang
 *
 * [7] 整数反转
 *
 * https://leetcode-cn.com/problems/reverse-integer/description/
 *
 * algorithms
 * Easy (32.23%)
 * Total Accepted:    112.3K
 * Total Submissions: 348.6K
 * Testcase Example:  '123'
 *
 * 给出一个 32 位的有符号整数，你需要将这个整数中每位上的数字进行反转。
 * 
 * 示例 1:
 * 
 * 输入: 123
 * 输出: 321
 * 
 * 
 * 示例 2:
 * 
 * 输入: -123
 * 输出: -321
 * 
 * 
 * 示例 3:
 * 
 * 输入: 120
 * 输出: 21
 * 
 * 
 * 注意:
 * 
 * 假设我们的环境只能存储得下 32 位的有符号整数，则其数值范围为 [−2^31,  2^31 − 1]。请根据这个假设，如果反转后整数溢出那么就返回
 * 0。
 * 
 */

func reverse(x int) int {
	// 存储数字的每一位
	res := make([]int,0)

	// 结果
	var re int = 0
	// 记录数正负
	var f int = 1
	// 如果等于0直接返回
	if x == 0 {
		return x
	}
	// 小于0将x转为为证书记录负号
	if x < 0 {
		f = -1
		x = x * f
	}
	// 循环 得到数的每一位
	// 除以10得余数 第一个得到的就是个位 然后是十位 百位 千位
	// 得到余数的同时将x除以10 
	// 然后循环得到每个数
	for {
		if x <= 0 {
			break
		}
		res = append(res, x % 10)
		x = x / 10

	}
	// 循环得到原有的数的每一位
	// 用这个数 加上已经得到的数再乘以10

	for i:= 0;i<len(res);i++{
		re = res[i]+re*10
	}
	// 然后乘以f 恢复其如果是负数
	// return re*f
	if  -(1 << 31)<= re * f && re * f <= ((1 << 31)-1 ) {
		return re*f
	}
	return 0
}