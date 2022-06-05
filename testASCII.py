string1 = 'P40'
if not string1.isdigit():
    num = ord(string1[0].upper())-ord('A')
    num+=10
    string1=str(num)+string1[1:]
string1 = int(string1)
string1 = "%04d"%string1
print(string1)