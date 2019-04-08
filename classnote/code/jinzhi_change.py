def change_stack(num, s):
    '''进值转换'''
    stack = []
    digit = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
    while num>0:
        stack.append(digit[num%s])
        num = num//s
    return ''.join([stack.pop() for i in range(len(stack))])



print(change_stack(89,2))
