/*
 * @lc app=leetcode.cn id=155 lang=golang
 *
 * [155] 最小栈
 *
 * https://leetcode-cn.com/problems/min-stack/description/
 *
 * algorithms
 * Easy (49.32%)
 * Likes:    249
 * Dislikes: 0
 * Total Accepted:    35.8K
 * Total Submissions: 72.5K
 * Testcase Example:  '["MinStack","push","push","push","getMin","pop","top","getMin"]\n[[],[-2],[0],[-3],[],[],[],[]]'
 *
 * 设计一个支持 push，pop，top 操作，并能在常数时间内检索到最小元素的栈。
 * 
 * 
 * push(x) -- 将元素 x 推入栈中。
 * pop() -- 删除栈顶的元素。
 * top() -- 获取栈顶元素。
 * getMin() -- 检索栈中的最小元素。
 * 
 * 
 * 示例:
 * 
 * MinStack minStack = new MinStack();
 * minStack.push(-2);
 * minStack.push(0);
 * minStack.push(-3);
 * minStack.getMin();   --> 返回 -3.
 * minStack.pop();
 * minStack.top();      --> 返回 0.
 * minStack.getMin();   --> 返回 -2.
 * 
 * 
 */
type MinStack struct {
	nums []int	 // 
	minindex []int // 记录每一次的索引
}


/** initialize your data structure here. */
func Constructor() MinStack {
    return MinStack{
		nums: make([]int,0),
		minindex: make([]int,0),
	}
}


func (this *MinStack) Push(x int)  {
	this.nums = append(this.nums,x)
	if len(this.minindex) == 0 || x <= this.nums[this.minindex[len(this.minindex)-1]] { // 最小值发生变化
		this.minindex = append(this.minindex,len(this.nums)-1) 
	}
}


func (this *MinStack) Pop()  {
	minc := len(this.minindex) - 1
	numcount := len(this.nums) - 1

	// 当前的值是最小值 将最小的值的最后一个元素删除
	if this.nums[this.minindex[minc]] == this.nums[numcount] {
		this.minindex = this.minindex[:minc]
	} 
	this.nums = this.nums[:numcount]

}


func (this *MinStack) Top() int {
	numcount := len(this.nums) - 1
	return this.nums[numcount]
}


func (this *MinStack) GetMin() int {
	if len(this.nums) == 0 {
		return 0
	}
	minc := len(this.minindex) - 1
	return this.nums[this.minindex[minc]]
}


/**
 * Your MinStack object will be instantiated and called as such:
 * obj := Constructor();
 * obj.Push(x);
 * obj.Pop();
 * param_3 := obj.Top();
 * param_4 := obj.GetMin();
 */

