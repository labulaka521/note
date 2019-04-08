class Solution:

    # infix_operatos = '+-*/()'

    def infix_to_postix(self, s):
        '中缀表达式转换为后缀表达式'
        infix_operatos = '+-*/()'
        st = list()  # 临时存放运算符
        exp = list()
        s = s.replace(' ', '')
        last = ''
        pri = {
            '(': 0,
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2,
        }
        for item in s:
            if item not in infix_operatos:
                # 数字直接进入表达式
                if last == 'num':
                    new_num = str(int(exp.pop())*10+int(item))
                    exp.append(new_num)
                else:
                    exp.append(item)
                last = 'num'
            elif len(st) == 0 or item == '(':
                # 缓存栈为空或者当前处理元素为左括号就可以直接入栈
                st.append(item)
                last = 'str'
            elif item == ')':
                # 当前处理运算符号是右括号，需要将此右括号前至第一个遇到的左括号之间的符号全部推进临时运算符存放
                # 缓存栈不为空并且栈顶的运算符也不为左括号
                while len(st) != 0 and st[-1] != '(':
                    exp.append(st.pop())
                st.pop()
                last = 'str'
            else:
                # 运算符号 比较与栈顶符号的优先级
                while len(st) != 0 and pri[st[-1]] >= pri[item]:
                    # 当前运算符优先级小于栈顶的优先级 将栈顶弹出添加到表达式 然后将当前运算符加入栈中
                    exp.append(st.pop())
                st.append(item)
                last = 'str'
        while len(st) != 0:
            exp.append(st.pop())
        return self.suf_exp_evalucator(exp)

    def cal(self, num1, optr, num2):
        if optr == '+':
            return num1 + num2
        elif optr == '-':
            return num1 - num2
        elif optr == '*':
            return num1 * num2
        elif optr == '/':
            return num1 / num2

    def suf_exp_evalucator(self, exp):
        infix_operatos = '+-*/()'
        if len(exp) == 1:
            return int(exp[0])
        st = list()         # 存放数字
        for item in exp:
            if item not in infix_operatos:          # 数字为
                st.append(item)
            else:
                num2 = int(st.pop())
                num1 = int(st.pop())
                new_num = self.cal(num1, item, num2)
                st.append(new_num)
        return st[0]


S = input()
r = Solution()
print(r.infix_to_postix(S))
