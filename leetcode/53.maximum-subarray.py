#
# @lc app=leetcode.cn id=53 lang=python3
#
# [53] 最大子序和
#
# https://leetcode-cn.com/problems/maximum-subarray/description/
#
# algorithms
# Easy (39.52%)
# Total Accepted:    25.9K
# Total Submissions: 65.3K
# Testcase Example:  '[-2,1,-3,4,-1,2,1,-5,4]'
#
# 给定一个整数数组 nums ，找到一个具有最大和的连续子数组（子数组最少包含一个元素），返回其最大和。
# 
# 示例:
# 
# 输入: [-2,1,-3,4,-1,2,1,-5,4],
# 输出: 6
# 解释: 连续子数组 [4,-1,2,1] 的和最大，为 6。
# 
# 
# 进阶:
# 
# 如果你已经实现复杂度为 O(n) 的解法，尝试使用更为精妙的分治法求解。
# 
#
class Solution:
    def maxSubArray(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        # onesum = 0
        # maxsum = nums[0]
        # if max(nums) < 0:
        #     return max(nums)

        # for i in range(len(nums)):          
        #     # 使用maxsum来记录当前字串最大值 使用onesum记录maxsum+一个元素的最大值 取两者最大值
        #     onesum += nums[i]
        #     maxsum = max(maxsum,onesum)
        #     if onesum < 0:
        #         onesum = 0
        # return maxsum
        for i in range(1, len(nums)):
            maxsum = max(nums[i]+nums[i-1], nums[i])    # 比较当前的元素值 与 当前元素值加上前序列最大子序 的大小 取最大
            nums[i] = maxsum    #  将此项修改为从开始到i的最大序列总和
        return max(nums)
        
