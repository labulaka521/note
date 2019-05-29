# LRU cache (Latest recently used)
# 
# LRU：least recently used，最近最少使用算法。其实就是按使用时间倒排序，然后从尾部删除元素。
# 它的使用场景是：在有限的空间中存储对象时，当空间满时，会按一定的原则删除原有的对象，常用的原则（算法）有LRU，FIFO，LFU等。
# 在计算机的Cache硬件，以及主存到虚拟内存的页面置换，还有Redis缓存系统中都用到了该算法。
# 当并发时 必须对set加锁

class LRUCache:
    
    def __init__(self, maxsize):
        self.maxsize = maxsize
        self.tm = 0
        self.cache = {}         # 存储缓存数据
        self.lru = {}           # 存储key 与其优先级
    
    def get(self, key):
        '''访问的时候会将其key的优先级升高r
        param key: key

        '''
        if key in self.cache:
            self.lru[key] = self.tm
            self.tm += 1
            # print(self.cache, self.lru)
            return self.cache[key]
        return -1
    
    def set(self, key, value):
        '''
        查找当前缓存数量是否大于缓存的最大数量
        大于则找到self.lru中优先级最小的删除后，然后执行增加操作
        '''
        if len(self.cache) >= self.maxsize:
            old_key = min(self.lru.keys(), key=lambda k: self.lru[k])
            self.cache.pop(old_key)
            self.lru.pop(old_key)
        self.cache[key] = value
        self.lru[key] = self.tm
        self.tm += 1
        print(self.cache, self.lru)


l = LRUCache(5)
l.set('a', 1)
l.set('b', 2)
l.set('c', 3)
l.set('d', 4)
l.set('e', 5)

print(l.get('a'))


# get 是O(1)的操作 
# set 因为有min(self.lru.keys(), key=lambda k: self.lru[k]) 所有时间复杂度为O(n)


# 使用OrderedDict来实现LRU缓存算法
# 这是一个有序的字典，

import collections

def LRUCache_v2:
    def __init__(self, maxsize):
        self.maxsize = maxsize
        self.cache = collections.OrderedDict()

    def get(self, key):
        '''
        首先弹出此key的值，然后重新入队，这时此key会被放在有序字典的最后 
        param key: 查找的key
        '''
        try:
            value = self.cache.pop(key)
            self.cache[key] = value
            return value
        except KeyError:
            return -1

    def set(self, key, value):
        '''
        先弹出key 如果没有此key 则比较缓存大小 比maxsize大则删除有序字典第一个元素
        然后设置key和value
        '''
        try:
            self.cache.pop(key)
        except KeyError:
            if len(self.cache) >= self.maxsize:
                self.cache.popitem(last=False)
                # LIFO order if last is true or FIFO order if false
        self.cache[key] = value
