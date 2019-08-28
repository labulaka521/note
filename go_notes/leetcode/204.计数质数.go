/*
 * @lc app=leetcode.cn id=204 lang=golang
 *
 * [204] 计数质数
 *
 * https://leetcode-cn.com/problems/count-primes/description/
 *
 * algorithms
 * Easy (29.26%)
 * Likes:    184
 * Dislikes: 0
 * Total Accepted:    23.8K
 * Total Submissions: 80.8K
 * Testcase Example:  '10'
 *
 * 统计所有小于非负整数 n 的质数的数量。
 * 
 * 示例:
 * 
 * 输入: 10
 * 输出: 4
 * 解释: 小于 10 的质数一共有 4 个, 它们是 2, 3, 5, 7 。
 * 
 * 
 */
func countPrimes(n int) int {
	// 时间复杂度过大
	// var count int

    // for i:=2;i<n;i++{
	// 	var yes bool
	// 	for j := 2;j <i-1;j++{
	// 		if i % j == 0 {
	// 			yes = true
	// 			break // 如果已经发生整除则直接跳出
	// 		}
	// 	}·
	// 	if yes == false {
	// 		count ++
	// 	}
	// }
	// return count

	noprimes := make([]bool,n)
	for i:=2;i<=int(math.Sqrt(float64(n))); i++ {
		// 求n的2次方
		// i为2的话 i * i,i* (i+1),i*(i+2)等都不是质数
		for j := i * i; j < n; j += i {
			noprimes[j] = true 
		}
	}
	count  := 0
	for i:=2;i<n;i++{
		if noprimes[i] == false {
			count ++
		}
	}
	return count
}

