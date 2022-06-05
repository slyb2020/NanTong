a = " ab-cd "
a = a.replace('-','')
print((a.strip()+"123").upper())



L1 = [1, ('a', 3)] # same value, unique objects
L2 = [1, ('a', 3)]
print(L1 == L2, L1 is L2) # equivalent?, same object?

