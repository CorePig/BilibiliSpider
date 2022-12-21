import copy

N = 1010
s = [['\0']*N for j in range(N)];
res = [[[False, False,False] for j in range(N)] for i in range(N)]
xd = [1, -1, 0, 0];
yd = [0, 0, 1, -1];
horse = [[1, 2], [1, -2], [2, 1], [2, -1], [-1, -2], [-1, 2], [-2, -1], [-2, 1]]
node = {"x": 0, "y": 0, "bs": 0, "val": 0}
n,m = map(int,input().split())
n, m = m, n
for i in range(n):
    temp = input()
    for i in range(len(temp)):
        s[i][i]=temp[i]
q = []
q.append(copy.deepcopy(node))
while q:
    fr = q[0]
    # print(type(fr))
    x = fr['x']
    y = fr["y"]
    bs = fr["bs"]
    val = fr["val"]
    res[x][y][val] = 1
    if x == n - 1 and y == m - 1:
        print(bs, end="")
        exit(0)
    q.pop(0)
    if val == 0:
        for i in range(4):
            xx = x + xd[i]
            yy = y + yd[i]
            if not (xx >= 0 and xx < n and yy >= 0 and yy < m):
                continue
            if res[xx][yy][val] or s[xx][yy] == 'X':
                continue
            q.append({"x":xx, "y":yy, "bs":(bs + 1), "val":val})
    else:
        for i in range(8):
            xx = x + horse[i][0];
            yy = y + horse[i][1];
            if not (xx >= 0 and xx < n and yy >= 0 and yy < m):
                continue;
            if res[xx][yy][val] or s[xx][yy] == 'X':
                continue;
            q.append({xx, yy, bs + 1, val})
    if s[x][y] == 'S':
        if res[x][y][val ^ 1] == 0:
            q.push({x, y, bs + 1, val ^ 1})
