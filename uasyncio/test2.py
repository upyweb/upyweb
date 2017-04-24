import uheapq as heapq

h = []

fl = True
#fl = False

vals = [200, 250, 255, 0, 1, 3, 10, 20]
#vals = [255, 0]
#vals = [0, 1, 2, 3, 4, 5]

for v in vals:
    heapq.heappush(h, (v,), fl)

print(h, "=======")


while h:
    print(heapq.heappop(h, fl))
