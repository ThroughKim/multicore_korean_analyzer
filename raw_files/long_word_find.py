f = open("total", "r")
lines = f.readlines()
for line in lines:
    words = line.split(" ")
    for word in words:
        if len(word) > 20:
            print(word)
