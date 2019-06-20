# LR文法分析表构造器
在`main.py`中配置对应的文法、终结符、非终结符、开始项目、开始符号即可自动生成项目集、GO关系、LR0分析表。
当生成LR0分析表产生冲突时，会自动构造FIRST集和FOLLOW集，转为生成SLR1分析表。

# 用法
`python3 main.py`
最后的表格如果需要输出到EXCEL中，建议稍作更改输出为CSV文件，再由EXCEL处理。

# 示例
对文法G[E]构造分析表
- E→E+T | E-T | T
- T→T*F | T/F | F
- F→P^F | P
- P→(E) | i*

应先构造其拓广文法G[E']，但此程序暂不支持两个字符的非终结符，因此用G[A]代替。
构造如下：
- A→E
- E→E+T
- E→E-T
- E→T
- T→T*F
- T→T/F
- T→F
- F→P^F
- F→P
- P→(E)
- P→i

然后如main.py最上方所示，写入列表中。
可知开始项目集为`A→·E`，开始符号为`A`
运行程序即可。