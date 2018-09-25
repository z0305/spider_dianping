

案例介绍：https://mp.weixin.qq.com/s/dkaV4VZ1QBzcsi9gXvCRdw (Python告诉你上海有哪些高性价比的西餐厅)
源码下载：https://github.com/pythonml/restaurant

# 默认是智能排序(o1), 好评是o3, 人气是o2, 口味是o4

# 当选定一个地方后, 首先选择美食分类和热门商区,
# 然后再根据美食分类爬虫, 至少两页
# 也可以选择按热门商区分类爬虫, 至少两页
# 最后可以将结果保存到db中, 并去重处理
# 爬虫结果肯定会有重复，使用db也可以去重



# 网站渲染后的结果可能用了不同的编码方式, 要充分考虑
# 719: <span id="avgPriceTitle" class="item">
#         人均：
#         <span class="fn-Kwvz"></span>
#         1
#         <span class="fn-JEFc"></span>元</span>
# 276: <span id="avgPriceTitle" class="item">
#         人均:
#         <span class="fn-cMXT"></span>
#         <span class="fn-Kwvz"></span>
#         <span class="fn-QanZ"></span>
#         元</span>


