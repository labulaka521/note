/*
 * @lc app=leetcode.cn id=119 lang=golang
 *
 * [119] 杨辉三角 II
 *
 * https://leetcode-cn.com/problems/pascals-triangle-ii/description/
 *
 * algorithms
 * Easy (56.86%)
 * Likes:    76
 * Dislikes: 0
 * Total Accepted:    19.2K
 * Total Submissions: 33.7K
 * Testcase Example:  '3'
 *
 * 给定一个非负索引 k，其中 k ≤ 33，返回杨辉三角的第 k 行。
 * 
 * 
 * 
 * 在杨辉三角中，每个数是它左上方和右上方的数的和。
 * 
 * 示例:
 * 
 * 输入: 3
 * 输出: [1,3,3,1]
 * 
 * 
 * 进阶：
 * 
 * 你可以优化你的算法到 O(k) 空间复杂度吗？
 * 
 */
func getRow(rowIndex int) []int {
	// 方法一 空间复杂度比较大
	// res := [][]int{}
	// res = append(res,[]int{1})
	// // 每一行的值是都是前一个数组的相同位置的值加上前一个数组相同位置-1处的值
	// // 如果没有就不加
	// // numRow-1轮循环 
	// // 从构建二行开始
	// for i:=1;i<=rowIndex;i++{
	// 	// 第几行就有几个数
	// 	item := make([]int,0)
	// 	for j :=0;j<=i;j++{
	// 		// 
	// 		var add int
	// 		// 第一行和最后一行的值为1
	// 		if j == 0 || j == i {
	// 			add = 1
	// 		} else {
	// 			// 取前一个数组的相同位置和前一位置的相加和的值
	// 			add = res[i-1][j]+res[i-1][j-1]
	// 		}
	// 		item = append(item,add)
	// 	}
	// 	res = append(res,item)
	// }
	// return res[rowIndex]
	// 方法二
	// O(k)
	// 直接在原数组中修改
	res := make([]int,rowIndex+1)
	res[0]=1
	for i:=1;i<=rowIndex;i++{
		var change int
		// 底层循环从后往前 这样才不会影响前面的值
		for j:=i;j>0;j--{
			if j == i {
				change = 1
			} else {
				change = res[j-1]+res[j]
			}
			res[j] = change
		}
	}
	return res
}

