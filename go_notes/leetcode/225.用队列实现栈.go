/*
 * @lc app=leetcode.cn id=225 lang=golang
 *
 * [225] 用队列实现栈
 *
 * https://leetcode-cn.com/problems/implement-stack-using-queues/description/
 *
 * algorithms
 * Easy (59.58%)
 * Likes:    63
 * Dislikes: 0
 * Total Accepted:    15.2K
 * Total Submissions: 25.5K
 * Testcase Example:  '["MyStack","push","push","top","pop","empty"]\n[[],[1],[2],[],[],[]]'
 *
 * 使用队列实现栈的下列操作：
 * 
 * 
 * push(x) -- 元素 x 入栈
 * pop() -- 移除栈顶元素
 * top() -- 获取栈顶元素
 * empty() -- 返回栈是否为空
 * 
 * 
 * 注意:
 * 
 * 
 * 你只能使用队列的基本操作-- 也就是 push to back, peek/pop from front, size, 和 is empty
 * 这些操作是合法的。
 * 你所使用的语言也许不支持队列。 你可以使用 list 或者 deque（双端队列）来模拟一个队列 , 只要是标准的队列操作即可。
 * 你可以假设所有操作都是有效的（例如, 对一个空的栈不会调用 pop 或者 top 操作）。
 * 
 * 
 */
type MyStack struct {
    s []int
}


/** Initialize your data structure here. */
func Constructor() MyStack {
	s := make([]int,0)
	return MyStack{s:s}
}


/** Push element x onto stack. */
func (this *MyStack) Push(x int)  {
	this.s = append(this.s,x)
}


/** Removes the element on top of the stack and returns that element. */
func (this *MyStack) Pop() int {
	if len(this.s) ==0 {
		return 0
	}
	i := this.Top()
	this.s = this.s[:len(this.s)-1]
	return i
}


/** Get the top element. */
func (this *MyStack) Top() int {
	if len(this.s) == 0 {
		return 0
	}
	i := this.s[len(this.s)-1]
	return i
}


/** Returns whether the stack is empty. */
func (this *MyStack) Empty() bool {
    if len(this.s) == 0 {
		return true
	}
	return false
}


/**
 * Your MyStack object will be instantiated and called as such:
 * obj := Constructor();
 * obj.Push(x);
 * param_2 := obj.Pop();
 * param_3 := obj.Top();
 * param_4 := obj.Empty();
 */

