/*
 * @lc app=leetcode.cn id=53 lang=golang
 *
 * [53] 最大子序和
 */
func maxSubArray(nums []int) int {
	var maxsum, cursum int
	maxsum = nums[0]
	for _, value := range nums {
		cursum += value          // cursum会一直增加
		if cursum > maxsum {	// 比较加一个数后和当前的最大值哪个大
			maxsum = cursum  // 保存当前的最大值
		}
		if cursum < 0 {		// 如果当前的总和为负数 就将当前的值设置为0 以保证与下一个数相加时 不会减小
			cursum = 0
		}
	}
	return maxsum
}

