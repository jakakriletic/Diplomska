string = "jaka je mega kul"
st = string.count("j", 0, len(string))
print(st)

test = string.endswith("kul")
print(test)

najdi = string.find("j")
print(najdi)

count = 0
for i in string:
    if i=="j":
        count += 1
print(count)