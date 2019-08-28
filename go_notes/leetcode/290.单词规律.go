/*
 * @lc app=leetcode.cn id=290 lang=golang
 *
 * [290] 单词规律
 *
 * https://leetcode-cn.com/problems/word-pattern/description/
 *
 * algorithms
 * Easy (39.95%)
 * Likes:    93
 * Dislikes: 0
 * Total Accepted:    10.4K
 * Total Submissions: 25.9K
 * Testcase Example:  '"abba"\n"dog cat cat dog"'
 *
 * 给定一种规律 pattern 和一个字符串 str ，判断 str 是否遵循相同的规律。
 * 
 * 这里的 遵循 指完全匹配，例如， pattern 里的每个字母和字符串 str 中的每个非空单词之间存在着双向连接的对应规律。
 * 
 * 示例1:
 * 
 * 输入: pattern = "abba", str = "dog cat cat dog"
 * 输出: true
 * 
 * 示例 2:
 * 
 * 输入:pattern = "abba", str = "dog cat cat fish"
 * 输出: false
 * 
 * 示例 3:
 * 
 * 输入: pattern = "aaaa", str = "dog cat cat dog"
 * 输出: false
 * 
 * 示例 4:
 * 
 * 输入: pattern = "abba", str = "dog dog dog dog"
 * 输出: false
 * 
 * 说明:
 * 你可以假设 pattern 只包含小写字母， str 包含了由单个空格分隔的小写字母。    
 * 
 */
func wordPattern(pattern string, str string) bool {
	// 将字符串转化为这个字符在这个字符串的第一个地方出现的index值
	pmap := make(map[rune]string)
	smap := make(map[string]string)
	var pp string
	var ss string
	for i,v := range pattern {
		_,ok := pmap[v]
		if !ok {
			pmap[v] = fmt.Sprintf("%d",i)
		}
		pp += pmap[v]
	}
	sp := strings.Split(str, " ")
	for i := 0; i < len(sp); i ++ {
		_,ok := smap[sp[i]]
		if !ok {
			smap[sp[i]] = fmt.Sprintf("%d",i)
		}
		ss += smap[sp[i]]
	}


	return ss == pp
}

