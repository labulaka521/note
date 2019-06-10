/*
 * @lc app=leetcode.cn id=35 lang=golang
 *
 * [35] 搜索插入位置
 */
func searchInsert(nums []int, target int) int {
	var i int
    for i < len(nums) {
		if nums[i] >= target {
			return i
		}
		i ++
	}
	return i
}

