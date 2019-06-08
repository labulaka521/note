/*
 * @lc app=leetcode.cn id=20 lang=golang
 *
 * [20] 有效的括号
 */
func isValid(s string) bool {
    if s == "" {
		return true
	}
	if len(s) % 2 != 0 {
		return false
	}
	// 入栈 右括号
	// k1 := map[int32]string{
	// 	123: "{",
	// 	91: "[",
	// 	40: "(",
	// }

	// kuohao := map[int32]string{
	// 	125: "{",
	// 	93: "[",
	// 	41: "(",
	// }
	
	// store := make([]string,0,100)
	// for _, i := range s {
	// 	if si, ok := kuohao[i]; ok {
	// 		if len(store) != 0 && si == store[len(store)-1] {
	// 			store = store[:len(store)-1]
	// 		} else {
	// 			return false
	// 		}
	// 	} else {
	// 		store = append(store,k1[i])
	// 	}

	// }
	// if len(store) == 0 {
	// 	return true
	// }
	// return false
	
	kh := map[rune]rune{
		'}':'{',
		']':'[',
		')':'(',
	}
	stack := make([]rune,0,100)
	for _, i := range s {
		switch i {
		case 123,91,40:
			stack = append(stack,i)
		default:
			if len(stack) == 0 {
				return false
			}
			if kh[i] != stack[len(stack)-1] {
				return false
			}
			stack = stack[:len(stack)-1]
		}
	}
	return len(stack) == 0

}

