#!/usr/bin/python

import sys
q = map(int, sys.argv[1:])
q = sorted(q, reverse=True)
while sum(q)>=40:
	c = [0]
	while c:
		s = sum(q[i] for i in c)
		if s==40:
			break

		f = False
		for i in range(c[-1]+1, len(q)):
			if s+q[i]==40 or s+q[i]+q[-1]<=40:
				c.append(i)
				f = True
				break
		if f:
			continue

		while c:
			n = q[c[-1]]
			for i in range(c[-1]+1, len(q)):
				if q[i]!=n:
					c[-1] = i
					f = True
					break
			if f:
				break

			c.pop()

	if not c:
		break

	print("Found 40% combination: {}".format(" ".join([str(q[i]) for i in c])))
	q = [q[i] for i in range(len(q)) if i not in c]

print("Leftovers: {}".format(" ".join(str(n) for n in q)))
