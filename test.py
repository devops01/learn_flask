# coding:utf-8
class fab(object):
    
    def __init__(self, num):
        self.max = num
        self.n, self.a, self.b = 0, 0, 1
    
    def __iter__(self):
        return self
    
    def next(self):
        if self.n < self.max:
            r = self.b
            self.a, self.b = self.b, self.a + self.b
            self.n = self.n + 1
            return r
        raise StopIteration

if __name__ == '__main__':
    # for n in fab(10):
    #     print n
    from pyecharts import Bar
    bar = Bar("我的第一个图表", "这里是副标题")
    attr = ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
    v1 = [5, 20, 36, 10, 75, 90]
    v2 = [8, 25, 18, 13, 30, 80]
    bar.add("商家A", attr, v1, mark_point=["average", "min", "max"])
    bar.add("商家B", attr, v2, mark_line=["min", "max"])
    bar.show_config()
    bar.render()