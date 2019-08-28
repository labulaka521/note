/*
 * @lc app=leetcode.cn id=121 lang=golang
 *
 * [121] 买卖股票的最佳时机
 *
 * https://leetcode-cn.com/problems/best-time-to-buy-and-sell-stock/description/
 *
 * algorithms
 * Easy (50.27%)
 * Likes:    463
 * Dislikes: 0
 * Total Accepted:    60.2K
 * Total Submissions: 119.6K
 * Testcase Example:  '[7,1,5,3,6,4]'
 *
 * 给定一个数组，它的第 i 个元素是一支给定股票第 i 天的价格。
 * 
 * 如果你最多只允许完成一笔交易（即买入和卖出一支股票），设计一个算法来计算你所能获取的最大利润。
 * 
 * 注意你不能在买入股票前卖出股票。
 * 
 * 示例 1:
 * 
 * 输入: [7,1,5,3,6,4]
 * 输出: 5
 * 解释: 在第 2 天（股票价格 = 1）的时候买入，在第 5 天（股票价格 = 6）的时候卖出，最大利润 = 6-1 = 5 。
 * ⁠    注意利润不能是 7-1 = 6, 因为卖出价格需要大于买入价格。
 * 
 * 
 * 示例 2:
 * 
 * 输入: [7,6,4,3,1]
 * 输出: 0
 * 解释: 在这种情况下, 没有交易完成, 所以最大利润为 0。
 * 
 * 
 */
func maxProfit(prices []int) int {
	// // 两轮循环
	// var maxprofit int
	// for i:=0;i<len(prices);i++{
	// 	for j:=i+1;j<len(prices);j++ {
	// 		if prices[j] - prices[i] > maxprofit {
	// 			maxprofit = prices[j] - prices[i]
	// 		}
	// 	}
	// }
	// return maxprofit

	// 将价格绘制成图
	// 买卖股票的最好的时机就是在最低谷然后到最高谷之间
	// 所以维持两个变量 最低谷的值minprices 和最大的利润
	var minprices = 1000000000
	var maxprofit = 0
	for i:=0;i<len(prices);i++{
		// 最小的谷值
		if prices[i] < minprices {
			minprices = prices[i]
		}
		// 寻找最大的利润
		// 比较当前最大的利润和 当前价格与最小值的的
		// 如果小于 则更新最大利润
		if maxprofit < prices[i] - minprices {
			maxprofit = prices[i] - minprices 
		}
	}
	return maxprofit
}

