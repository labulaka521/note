/*
 * @lc app=leetcode.cn id=66 lang=golang
 *
 * [66] 加一
 */
// package main
// import (
// 	"fmt"
// )
// func main() {
// 	fmt.Println(plusOne([]int{9,9,9}))
// }
func plusOne(digits []int) []int {
	count := len(digits)

	for i:=count-1;i>=0;i-- {
		if digits[i]<9 {
			digits[i]+=1
			return digits
		} else {
			digits[i] = 0
		}
	}
	// 到这里的话则表示原始数组全是9
	a := make([]int,count + 1)
	a[0] = 1
	return a
}


