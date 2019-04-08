
def check_parens(text):
    '括号匹配配对函数，text是被检查的正文串'
    parens = "()[]{}"
    open_parens = "([{"
    opposite = {'}':'{', ')':'(',']':'['}
    def parentheses(text):
        '括号生成器 每次调用返回text里的下一括号及位置'
        i, text_len = 0, len(text)
        while True:
            while i < text_len and text[i] not in parens:
                i+=1
            if i >= text_len:
                return
            yield text[i], i
            i+=1

    st = list()
    for pr, i in parentheses(text):
        # 对text里各括号和位置迭代
        if pr in open_parens:
            st.append(pr)
        elif st.pop() != opposite[pr]:
            print(f'Unmatching is found at {i} for {pr}')
            return False
    print('All parentheses are corrently matched')
    return True

text = input()
check_parens(text)
