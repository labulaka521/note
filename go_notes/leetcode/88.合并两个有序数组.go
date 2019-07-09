/*
 * @lc app=leetcode.cn id=88 lang=golang
 *
 * [88] 合并两个有序数组
 */
func merge(nums1 []int, m int, nums2 []int, n int)  {
	// 将nums2追加到nums1 然后再排序
	nums1 = append(nums1[:m],nums2...)

	total := m + n

	for i :=0; i<total;i++{
		minindex := i
		for j:=i+1;j<total;j++ {
			if nums1[j] < nums1[minindex] {
				minindex = j
			}
		}
		tmp := nums1[minindex]
		nums1[minindex] = nums1[i]
		nums1[i] = tmp
	}
	return
}


