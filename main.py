# 程序使用Python3运行
# 示例文法G[E]：
# E→E+T | E-T | T
# T→T*F | T/F | F
# F→P^F | P
# P→(E) | i

# 用前需配置全局变量如下
# 拓广文法G[A]，必须写开，不能带或
C = ['A→E', 'E→E+T', 'E→E-T', 'E→T', 'T→T*F', 'T→T/F', 'T→F', 'F→P^F', 'F→P', 'P→(E)', 'P→i']
# 非终结符，必须是一个字符不能写成类似E'，不然转向SLR时会出错
Vn = ['A', 'E', 'T', 'F', 'P']
# 终结符，必须是一个字符，空字符写成ε
Vt = ['+', '-', '*', '/', '^', '(', ')', 'i', '#']
# 项目集的构造由此项目开始
begin = 'A→·E'
# 开始字符，如G[A]中就是A
BEGIN = 'A'



def findI(I, v):
	newI = []
	global C
	for i in range(len(I)):
		index = location(I[i])
		if index != -1 and I[i][index] == v:
			newI.append(getNextPointI(I[i]))
	addNewI(newI, C)
	return newI


def addNewI(newI, C):
	if newI == []:
		return
	oldLen = len(newI)
	for i in range(oldLen):
		index = location(newI[i])
		if index != -1 and isVn(newI[i][index]):
			for j in range(len(C)):
				if getKey(C[j]) == newI[i][index]:
					_ = addFirstPoint(C[j])
					if _ not in newI:
						newI.append(_)
	if oldLen != len(newI):
		addNewI(newI, C)


def location(i):
	index = i.index('·')
	if index != -1 and (index + 1) != len(i):
		return index + 1
	return -1


def getNextPointI(i):
	iArr = i.split('·')
	iArr[1] = iArr[1][0] + '·' + iArr[1][1:]
	return ''.join(iArr)


def isVn(i):
	global Vn
	if i in Vn:
		return True
	return False


def getKey(i):
	iArr = i.split('→')
	return iArr[0]


def addFirstPoint(i):
	iArr = i.split('→')
	iArr[1] = '·' + iArr[1]
	return '→'.join(iArr)


def printI(I):
	for i in I:
		print(i)
	print("")


def generateTable(GO, I):
	global Vt, Vn
	res = {}
	for k1 in range(len(I)):
		res[k1] = {}
		for k2 in Vt + Vn:
			res[k1][k2] = ' '

	for g in GO:
		for vt in Vt:
			if vt in g:
				addTd(res, g[0], g[1], g[2], 's')
		for vn in Vn:
			if vn in g:
				addTd(res, g[0], g[1], g[2], '')
	endI = getEndPointI()
	for i in range(1, len(endI)):
		for In in I:
			if endI[i] in In:
				for vt in Vt:
					if res[I.index(In)][vt] != '':
						print('检测到冲突，自动生成SLR表')
						generateSLRTable(GO, I)
						return
					addTd(res, I.index(In), vt, i, 'r')
	for In in I:
		if endI[0] in In:
			addTd(res, I.index(In), '#', 'acc', '')

	print("\n表：")
	print("", end = '\t')
	for k in Vt + Vn:
		if k == Vn[-1]:
			print(k)
		else:
			print(k, end = '\t')
	for k1 in res:
		print(str(k1), end ='\t')
		for k2 in res[k1]:
			print(res[k1][k2], end = '\t')
		print("")


def generateSLRTable(GO, I):
	print("生成FIRST集：")
	first = getFirst()
	print(first)
	print("生成FOLLOW集")
	follow = getFOLLOW(first)
	print(follow)
	global Vt, Vn
	res = {}
	for k1 in range(len(I)):
		res[k1] = {}
		for k2 in Vt + Vn:
			res[k1][k2] = ' '

	for g in GO:
		for vt in Vt:
			if vt in g:
				addTd(res, g[0], g[1], g[2], 's')
		for vn in Vn:
			if vn in g:
				addTd(res, g[0], g[1], g[2], '')
	endI = getEndPointI()
	for i in range(1, len(endI)):
		for In in I:
			if endI[i] in In:
				for vt in follow[endI[i].split('→')[0]]:
					if res[I.index(In)][vt] != '':
						addTd(res, I.index(In), vt, i, 'r')
	for In in I:
		if endI[0] in In:
			addTd(res, I.index(In), '#', 'acc', '')

	print("\n表：")
	print("", end = '\t')
	for k in Vt + Vn:
		if k == Vn[-1]:
			print(k)
		else:
			print(k, end = '\t')
	for k1 in res:
		print(str(k1), end ='\t')
		for k2 in res[k1]:
			print(res[k1][k2], end = '\t')
		print("")


def addTd(table, k, a, j, key):
	j = str(j)
	table[k][a] = key + j


def getEndPointI():
	global C
	endI = []
	for i in C:
		endI.append(i + '·')
	return endI


def getFirst():
	global C, Vt, Vn
	first = {}
	for i in C:
		first[i.split('→')[0]] = []
	while True:
		flag = False
		for i in C:
			key = i.split('→')[0]
			r1 = i.split('→')[1][0]
			if r1 in Vt or r1 == 'ε':
				if addInSet(first[key], r1) == True:
					flag = True
			if r1 in Vn:
				empty = 0
				for t in i.split('→')[1]:
					if t in Vn:
						if addInSet(first[key], [_ for _ in first[t] if _ != 'ε']) == True:
							flag = True
						if checkEmpty(t) == False:
							break
						else:
							empty += 1
					else:
						break
				if empty == len(i.split('→')[1]):
					if addInSet(first[key], 'ε') == True:
						flag = True
		if flag == False:
			break
	return first


def getFOLLOW(first):
	follow = {}
	global C, BEGIN
	for v in Vn:
		if v == BEGIN:
			follow[v] = set('#')
		else:
			follow[v] = set()
	while True:
		_flag = False
		for i in C:
			left = i.split('→')[0]
			right = i.split('→')[1]
			for index in range(len(right)):
				if right[index] in Vt or 'ε' in right[index]:
					continue
				if index == (len(right) - 1):
					for _ in follow[left]:
						lg = len(follow[right[index]])
						follow[right[index]].add(_)
						if lg < len(follow[right[index]]):
							_flag = True
				else:
					if right[index+1] in Vt:
						follow[right[index]].add(right[index+1])
						lg = len(follow[right[index]])
						if lg < len(follow[right[index]]):
							_flag = True
					else:
						for _ in first[right[index+1]]:
							if _ != 'ε':
								follow[right[index]].add(_)
								lg = len(follow[right[index]])
								if lg < len(follow[right[index]]):
									_flag = True
					flag = False
					for _ in right[index + 1:]:
						if (_ in Vt) or ('ε' not in first[_]):
							flag = True
					if flag == False:
						for _ in follow[left]:
							follow[right[index]].add(_)
							lg = len(follow[right[index]])
							if lg < len(follow[right[index]]):
								_flag = True

		if _flag == False:
			break
	return follow
			


def checkEmpty(v):
	global C
	for i in C:
		iArr = i.split('→')
		if iArr[0] == v and iArr[1] == 'ε':
			return True
	return False

def addInSet(arr, o):
	flag = False
	if type(o) == str:
		if o not in arr:
			flag = True
			arr.append(o)
	else:
		for m in o:
			if m not in arr:
				flag = True
				arr.append(m)
	return flag


def main():
	global begin, C
	I = []
	GO = []
	I0 = [begin]
	addNewI(I0, C)
	I.append(I0)
	print("添加I0:")
	printI(I[0])
	for In in I:
		for v in (Vn + Vt):
			newI = findI(In, v)
			if newI != []:
				thisI = I.index(In)
				if newI in I:
					GO.append([thisI, v, I.index(newI)])
				else:
					GO.append([thisI, v, len(I)])
					print("添加I" + str(len(I)) + ":")
					I.append(newI)
					printI(newI)
	print("GO关系:")
	for g in GO:
		print("GO(I" + str(g[0]) + ", " + g[1] + ") = I" + str(g[2]))
	generateTable(GO, I)

if __name__ == '__main__':
	main()