def is_yes_paren(par):
    '括号匹配算法'
    stack = []
    for i in par:
        if i == '(':
            stack.append(i)
        elif i == ')':
            stack.pop()
        else:
            return False
    return stack ==list()


par = input()
print(is_yes_paren(par))


# ➜  python python3 classnote/code/paren.py
# py
# (()()(()()))
# True
# ➜  python python3 classnote/code/paren.py
# (()((()()))
# False
