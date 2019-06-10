/*
 * @lc app=leetcode.cn id=38 lang=golang
 *
 * [38] 报数
 */
func countAndSay(n int) string {
	s := "1"
	for i:=1;i<=n;i++ {	
		lt, temp, count := s[0],"",0
		for j:=0;j <len(s); j ++ {
			if lt == s[j] {
				count ++
			} else {
				temp = fmt.Sprintf("%s%d%c", temp,count,lt)
				lt = s[j]
				count = 0
			}
		}
		temp = fmt.Sprintf("%s%d%c", temp, count, lt)
        s = temp
	}
	return s
}



