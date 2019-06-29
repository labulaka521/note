/*
 * @lc app=leetcode.cn id=69 lang=golang
 *
 * [69] x 的平方根
 */
func mySqrt(x int) int {
	var i int
    for {
		if i * i > x {
			return i-1
		}
		i ++
	}
}

