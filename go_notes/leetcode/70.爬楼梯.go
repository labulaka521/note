/*
 * @lc app=leetcode.cn id=70 lang=golang
 *
 * [70] 爬楼梯
 */
func climbStairs(n int) int {
	// res 1 暴力解法
	// return climb_Stairs(0,n)
	// 时间复杂度 2^n

	// res 2 
	// 假设爬n个台阶有f(n)种可能性
	// 如果爬一阶，剩下n-1有f(n-1)种可能性
	// 如果爬二阶，剩下n-2有(n-2)种可能性
	// f(n) = f(n-1) + f(n-2)
	// 斐波那契数列公式
	var i,j=1,1
	for a:=0;a < n-1;a++ {
		var tmp = i
		i = i + j
		j = tmp
	}
	return i
}
// func climb_Stairs(i,n int) int {
// 	if i > n {
// 		return 0
// 	}
// 	if i == n {
// 		return 1
// 	}
// 	return climb_Stairs(i+1,n) + climb_Stairs(i+2,n)
//  }

