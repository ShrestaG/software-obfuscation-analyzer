def heavy_task():
    total = 0
    for i in range(10000):
        for j in range(1000):
            total += i * j
    return total

print(heavy_task())