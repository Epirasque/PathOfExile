#!/usr/bin/python

def find_valid(q, b, s, t):
	for i in range(b, len(q)):
		if s+q[i]==t or s+q[i]+q[-1]<=t:
			return i

def increment(q, c):
	n = q[c[-1]]
	for i in range(c[-1]+1, len(q)):
		if q[i]!=n:
			c[-1] = i
			return True
	return False

def greedy(q, t):
	r = []
	while sum(q)>=t:
		c = [0]
		while c:
			s = sum(q[i] for i in c)
			if s==t:
				break

			i = find_valid(q, c[-1]+1, s, t)
			if i:
				c.append(i)
				continue

			while c:
				if increment(q, c):
					break

				c.pop()

		if not c:
			break

		r.append([q[i] for i in c])
		q = [q[i] for i in range(len(q)) if i not in c]

	return r, q

def pair_sums(q):
	return [(i, j, q[i]+q[j]) for i in range(0, len(q)-1) for j in range(i+1, len(q))]

def permute(r, q):
	p = pair_sums(q)
	for c in r:
		t = pair_sums(c)

		for x in t:
			for y in p:
				if x[2]==y[2] and q[y[0]]<c[x[0]]:
					c[x[0]], q[y[0]] = q[y[0]], c[x[0]]
					c[x[1]], q[y[1]] = q[y[1]], c[x[1]]
					return True

	return False

def main(q, v=False):
	q = sorted(q, reverse=True)

	if v:
		print("Input: {}".format(" ".join(str(n) for n in q)))

	r, q = greedy(q, 40)
	if v:
		print("Leftovers after initial round: {} (total {})".format(" ".join(str(n) for n in q), sum(q)))
	i = 0
	while sum(q)>40 and i<100:
		permute(r, q)
		i += 1
		n, q = greedy(q, 40)
		r += n
	for c in r:
		print("Found 40% combination: {}".format(" ".join([str(n) for n in c])))
	if q:
		print("Leftovers: {} (total {})".format(" ".join(str(n) for n in q), sum(q)))
	else:
		print("No leftovers")

def test():
	import random
	a = 5**0.5
	b = 20**0.5
	for k in range(100):
		q = [int((a+random.random()*(b-a))**2) for i in range(100)]
		if k:
			print("---")
		main(q, True)

if __name__=="__main__":
	import sys
	if sys.argv[1]=="--test":
		test()
	else:
		main(map(int, sys.argv[1:]))
