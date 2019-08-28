/*
 * @lc app=leetcode.cn id=205 lang=golang
 *
 * [205] 同构字符串
 *
 * https://leetcode-cn.com/problems/isomorphic-strings/description/
 *
 * algorithms
 * Easy (45.46%)
 * Likes:    125
 * Dislikes: 0
 * Total Accepted:    14.9K
 * Total Submissions: 32.8K
 * Testcase Example:  '"egg"\n"add"'
 *
 * 给定两个字符串 s 和 t，判断它们是否是同构的。
 * 
 * 如果 s 中的字符可以被替换得到 t ，那么这两个字符串是同构的。
 * 
 * 所有出现的字符都必须用另一个字符替换，同时保留字符的顺序。两个字符不能映射到同一个字符上，但字符可以映射自己本身。
 * 
 * 示例 1:
 * 
 * 输入: s = "egg", t = "add"
 * 输出: true
 * 
 * 
 * 示例 2:
 * 
 * 输入: s = "foo", t = "bar"
 * 输出: false
 * 
 * 示例 3:
 * 
 * 输入: s = "paper", t = "title"
 * 输出: true
 * 
 * 说明:
 * 你可以假设 s 和 t 具有相同的长度。
 * 
 */
func isIsomorphic(s string, t string) bool {
   // 统计s中相同字符串的个数，将重复
   	ss := staticStr(s)
   	tt := staticStr(t)
	if len(ss) != len(tt) {
		return false
	}
	// 判断是否相同
   	for i := range ss {
		for j := range tt {
			if len(ss[i]) == len(tt[j]) {
				if reflect.DeepEqual(ss[i],tt[j]) {
					delete(ss,i)
					delete(tt,j)
				}
			}
		}
	}
	if len(ss) == 0 && len(tt) == 0 {
		return true
	}
	return false
}

// 统计字符串的总数，并计算出他们的位置

func staticStr(s string) map[rune][]int {

	m :=make(map[rune][]int,len(s))

	for i,v:=range s {
		vsli,ok := m[v]
		if !ok {
			vsli = make([]int,0,len(s))
		}
		vsli = append(vsli,i)
		m[v] = vsli
	}
	for i := range m {
		if len(m[i]) == 1 {
			delete(m,i)
		}
	}
	return m
}

