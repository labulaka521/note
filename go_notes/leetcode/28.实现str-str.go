func strStr(haystack string, needle string) int {
    if needle == "" {
		return 0
	}
	// 直接匹配字符串 使用将haystack切片和待比较的字符串比较
	// 如果不相同就同时将start end+1
	start := 0

	countn := len(needle)
	counth := len(haystack)
	for {
		if start+countn > counth {
			return -1
		}
		if needle == haystack[start:start+countn] {
			return start
		}
		start ++
	}
}

