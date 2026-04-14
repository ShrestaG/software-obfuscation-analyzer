text = "hello world " * 100000

count = 0
for char in text:
    if char == "o":
        count += 1

print(count)