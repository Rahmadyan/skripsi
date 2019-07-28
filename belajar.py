L = [['a','bob'],['a','bob'],['a','john']]

for i, x in enumerate(L):
    for j, a in enumerate(x):
        print(a)
        if 'bob' in a:
            L = [[i, j if j != 'bob' else 'b'] for i, j in L]


# L = [[i, j if j != 'bob' else 'b'] for i, j in L]
# print(L)
