/*
 * @lc app=leetcode.cn id=58 lang=golang
 *
 * [58] 最后一个单词的长度
 */
func lengthOfLastWord(s string) int {
	var (
		count int
	)
	if s == "" {
		return 0
	}
	
	for i:=len(s)-1;i >=0 ;i-- {
		if string(s[i]) == " " && count != 0 {
			return count
		} else {
			if string(s[i]) != " " {
				count ++
			}
		}
	}
	return count
}

