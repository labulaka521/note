/*
 * @lc app=leetcode.cn id=118 lang=golang
 *
 * [118] 杨辉三角
 *
 * https://leetcode-cn.com/problems/pascals-triangle/description/
 *
 * algorithms
 * Easy (63.13%)
 * Likes:    172
 * Dislikes: 0
 * Total Accepted:    30.4K
 * Total Submissions: 48K
 * Testcase Example:  '5'
 *
 * 给定一个非负整数 numRows，生成杨辉三角的前 numRows 行。
 * 
 * 
 * 
 * 在杨辉三角中，每个数是它左上方和右上方的数的和。
 * 
 * 示例:
 * 
 * 输入: 5
 * 输出:
 * [
 * ⁠    [1],
 * ⁠   [1,1],
 * ⁠  [1,2,1],
 * ⁠ [1,3,3,1],
 * ⁠[1,4,6,4,1]
 * ]
 * 
 */
func generate(numRows int) [][]int {
	res := [][]int{}
	if numRows == 0 {
		return res
	}
	res = append(res,[]int{1})
	// 每一行的值是都是前一个数组的相同位置的值加上前一个数组相同位置-1处的值
	// 如果没有就不加
	// numRow-1轮循环 
	// 从构建二行开始
	for i:=1;i<numRows;i++{
		// 第几行就有几个数
		item := make([]int,0)
		for j :=0;j<=i;j++{
			// 
			var add int
			// 第一行和最后一行的值为1
			if j == 0 || j == i {
				add = 1
			} else {
				// 取前一个数组的相同位置和前一位置的相加和的值
				add = res[i-1][j]+res[i-1][j-1]
			}
			item = append(item,add)
		}
		res = append(res,item)
	}
	return res
}

