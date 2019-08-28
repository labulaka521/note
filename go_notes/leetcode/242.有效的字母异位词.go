/*
 * @lc app=leetcode.cn id=242 lang=golang
 *
 * [242] 有效的字母异位词
 *
 * https://leetcode-cn.com/problems/valid-anagram/description/
 *
 * algorithms
 * Easy (54.59%)
 * Likes:    100
 * Dislikes: 0
 * Total Accepted:    42.4K
 * Total Submissions: 76.7K
 * Testcase Example:  '"anagram"\n"nagaram"'
 *
 * 给定两个字符串 s 和 t ，编写一个函数来判断 t 是否是 s 的字母异位词。
 * 
 * 示例 1:
 * 
 * 输入: s = "anagram", t = "nagaram"
 * 输出: true
 * 
 * 
 * 示例 2:
 * 
 * 输入: s = "rat", t = "car"
 * 输出: false
 * 
 * 说明:
 * 你可以假设字符串只包含小写字母。
 * 
 * 进阶:
 * 如果输入字符串包含 unicode 字符怎么办？你能否调整你的解法来应对这种情况？
 * 
 */
func isAnagram(s string, t string) bool {
	check := [26]uint8{}

	tip := "a"
	for i:=0;i<len(s);i++{               
		check[s[i]-tip[0]] ++				// 统计字母的个数
	}
	for i:=0;i<len(t);i++{
		check[t[i]-tip[0]] --				// 减去字母的个数
	}
	for i:=0;i<26;i++{
		if check[i] != 0 {					// 判断数组的元素是否全部为0
			return false
		}
	}
	return true
}

