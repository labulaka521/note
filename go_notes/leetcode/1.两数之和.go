/*
 * @lc app=leetcode.cn id=1 lang=golang
 *
 * [1] 两数之和
 *
 * https://leetcode-cn.com/problems/two-sum/description/
 *
 * algorithms
 * Easy (45.74%)
 * Total Accepted:    334.7K
 * Total Submissions: 731.7K
 * Testcase Example:  '[2,7,11,15]\n9'
 *
 * 给定一个整数数组 nums 和一个目标值 target，请你在该数组中找出和为目标值的那 两个 整数，并返回他们的数组下标。
 * 
 * 你可以假设每种输入只会对应一个答案。但是，你不能重复利用这个数组中同样的元素。
 * 
 * 示例:
 * 
 * 给定 nums = [2, 7, 11, 15], target = 9
 * 
 * 因为 nums[0] + nums[1] = 2 + 7 = 9
 * 所以返回 [0, 1]
 * 
 * 
 */

func twoSum(nums []int, target int) []int {
	// Solution 1
	// 将每个数和其对应的索引存储在一个map中
	// 使用target减去当前循环的数，然后查看得到的数是否在map中
	// 如果存在则直接返回当前数的index 和从map中得到得数的值 这个值正是这个数在nums中的索引 3 2 4 6
	result := make([]int,2)
	hash := make(map[int]int,0)
	for i, num := range nums {
		index, ok := hash[target-num]
		if ok {
			result[0]=i
			result[1]=index
			return result
		}
		hash[num]=i
	}
	return result

	// Solution 1
	// 暴力循环每个数 两轮循环 然后判断索引不想等而且相加等于target 返回
	// var res []int
	// for i:=0; i<=len(nums)-1;i++ {
	// 	for j := 0; j <= len(nums)-1; j++ {
	// 		if i != j && nums[i]+nums[j] == target {
	// 			res = append(res,i,j)
	// 			return res
	// 		}
	// 	}
	// }
	// return []int{}
}

