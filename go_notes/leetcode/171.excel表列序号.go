/*
 * @lc app=leetcode.cn id=171 lang=golang
 *
 * [171] Excel表列序号
 *
 * https://leetcode-cn.com/problems/excel-sheet-column-number/description/
 *
 * algorithms
 * Easy (64.85%)
 * Likes:    77
 * Dislikes: 0
 * Total Accepted:    17.7K
 * Total Submissions: 27.3K
 * Testcase Example:  '"A"'
 *
 * 给定一个Excel表格中的列名称，返回其相应的列序号。
 * 
 * 例如，
 * 
 * ⁠   A -> 1
 * ⁠   B -> 2
 * ⁠   C -> 3
 * ⁠   ...
 * ⁠   Z -> 26
 * ⁠   AA -> 27
 * ⁠   AB -> 28 
 * ⁠   ...
 * 
 * 
 * 示例 1:
 * 
 * 输入: "A"
 * 输出: 1
 * 
 * 
 * 示例 2:
 * 
 * 输入: "AB"
 * 输出: 28
 * 
 * 
 * 示例 3:
 * 
 * 输入: "ZY"
 * 输出: 701
 * 
 * 致谢：
 * 特别感谢 @ts 添加此问题并创建所有测试用例。
 * 
 */
func titleToNumber(s string) int {
	// var res int
    // for i:=0;i<len(s);i++{
	// 	// AB 26*(26**1) + 25*(26**0)
	// 	ii := len(s)- 1 - i
	// 	res += int(s[ii]-64)*int(math.Pow(26,float64(ii)))
	// }
	// return res
	var res int
	for i:=0;i<len(s);i++{
		// AB 26*(26**1) + 25*(26**0)
		ln := int(s[i]-64)
		i1 := len(s)- 1 - i
		res += ln*int(math.Pow(26,float64(i1)))
	}

	return res
}

