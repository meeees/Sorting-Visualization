def bubble_sort(eles) :
	for i in range(0, len(eles)) :
		for j in range(0, len(eles) - 1) :
			if(eles[j] > eles[j + 1]) :
				tmp = eles[j]
				eles[j] = eles[j + 1]
				eles[j + 1] = tmp
		yield i
	yield -1

def insertion_sort(eles) :
	for i in range(1, len(eles)) :
		j = i
		while j > 0 and eles[j - 1] > eles[j] :
			tmp = eles[j]
			eles[j] = eles[j - 1]
			eles[j - 1] = tmp
			j -= 1
		yield i
	yield -1

def selection_sort(eles) :
	for i in range(0, len(eles) - 1) :
		minel = i
		for j in range(i, len(eles)) :
			if eles[minel] > eles[j] :
				minel = j
		if minel != i :
			tmp = eles[minel]
			eles[minel] = eles[i]
			eles[i] = tmp
		yield i
	yield -1

def quick_sort(eles, startInd = 0, endInd = None) :
	if endInd == None :
		endInd = len(eles) - 1
	if(endInd - startInd <= 1) :
		yield -1
	pivot = eles[endInd]
	lInd = startInd
	rInd = endInd - 1
	copy = eles[startInd:endInd]
	for x in range(0, len(copy)) :
		if(copy[x] > pivot) :
			eles[rInd] = copy[x]
			rInd -= 1
		else :
			eles[lInd] = copy[x]
			lInd += 1
		yield x
	eles.pop(endInd)
	eles.insert(lInd, pivot)
	yield 0
	left_iter = iter(quick_sort(eles, startInd, lInd - 1))
	i = left_iter.next()
	while i != -1 :
		yield i
		i = left_iter.next()
	right_iter = iter(quick_sort(eles, rInd + 1, endInd))
	i = right_iter.next()
	while i != -1 :
		yield i
		i = right_iter.next()
	yield -1

def merge(eles, left, right) :
	ind = left[0]
	left_copy = eles[left[0]:left[1]]
	right_copy = eles[right[0]:right[1]]
	while len(left_copy) != 0 and len(right_copy) != 0 :
		if(left_copy[0] > right_copy[0]) :
			eles[ind] = right_copy.pop(0)
		else :
			eles[ind] = left_copy.pop(0)
		ind += 1
		yield 0
	while len(left_copy) != 0 :
		eles[ind] = left_copy.pop(0)
		ind += 1
		yield 0
	while len(right_copy) != 0 :
		eles[ind] = right_copy.pop(0)
		ind += 1
		yield 0
	yield -1

def merge_sort(eles, startInd = 0, endInd = None) :
	if endInd == None :
		endInd = len(eles)
	if endInd - startInd <= 1 :
		yield -1
	lInds = (startInd, ((endInd - startInd) / 2) + startInd)
	rInds = (((endInd - startInd) / 2) + startInd, endInd)
	left_iter = iter(merge_sort(eles, startInd, lInds[1]))
	i = left_iter.next()
	while(i != -1) :
		yield i
		i = left_iter.next()
	right_iter = iter(merge_sort(eles, rInds[0], endInd))
	i = right_iter.next()
	while(i != -1) :
		yield i
		i = right_iter.next()
	merge_iter = merge(eles, lInds, rInds)
	i = merge_iter.next()
	while(i != -1) :
		yield i
		i = merge_iter.next()
	yield -1


def check_sorted(eles) :
	for x in range(0, len(eles) - 1) :
		if eles[x] > eles[x + 1] :
			return False
	return True

	