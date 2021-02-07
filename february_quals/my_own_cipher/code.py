import string

alph = string.ascii_uppercase
l = len(alph)

mess = input().upper()
key = int(input()) % l
sign = 1
res = ''

for c in mess:
    if c in alph:
        res += alph[(alph.find(c) + sign*key) % l]
    else:
        res += c
    sign = -1*sign
    key=(key+1)%l

print(res)
