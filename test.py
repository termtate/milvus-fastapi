from towhee import pipe

a = (pipe.input("a").output("a"))

b = a(1)
print(b.to_list(kv_format=True))
    

