/*
 * @lc app=leetcode.cn id=125 lang=golang
 *
 * [125] 验证回文串
 *
 * https://leetcode-cn.com/problems/valid-palindrome/description/
 *
 * algorithms
 * Easy (40.48%)
 * Likes:    97
 * Dislikes: 0
 * Total Accepted:    45K
 * Total Submissions: 111.1K
 * Testcase Example:  '"A man, a plan, a canal: Panama"'
 *
 * 给定一个字符串，验证它是否是回文串，只考虑字母和数字字符，可以忽略字母的大小写。
 * 
 * 说明：本题中，我们将空字符串定义为有效的回文串。
 * 
 * 示例 1:
 * 
 * 输入: "A man, a plan, a canal: Panama"
 * 输出: true
 * 
 * 
 * 示例 2:
 * 
 * 输入: "race a car"
 * 输出: false
 * 
 * 
 */
func isPalindrome(s string) bool {
	s1 :=[]string{}
	// 将所有的大写字母转化为小写
	// 将标点符号空格去除
	for _,i := range s {
		if ("a" <= string(i) && string(i) <= "z") || ("A" <= string(i) && string(i) <= "Z") || ("0" <= string(i) && string(i) <= "9") {
			if string(i) < "a" {
				i += 32
			}
			s1 = append(s1,string(i))
		}	
	}
	start,end :=0, len(s1)-1
	for start < end {
		if s1[start] != s1[end] {
			return false
		}
		start ++
		end --
	}
	return true
}

