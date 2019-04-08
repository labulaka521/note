import random
def insertsort(lst):
    for i in range(1, len(lst)):
        # j = 0
        for j in range(i):
            if lst[i] < lst[j]:
                data = lst.pop(i)
                print(lst[j])
                lst.insert(j,data)
                
                break
    return lst

a = [2,1,3]
# for i in range(5):
#     a.append(random.randrange(10000))
#     # a.append(i)

print(a,'\n',insertsort(a))
