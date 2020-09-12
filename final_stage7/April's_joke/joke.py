from goto import goto, label

flager=1
ind  = [1,4,10,13,17,19]
txt = "______________tg_eu_eht_yw_n"
smt = [0,3,8,7,0,0]
label .start
new_str = ""
glob_ind = 0
flag1 = ["N","O","H","T","R","E","B","Y","C"]
for i in xrange(100):
    goto .go
    for q in xrange(25):
        goto .start
        print q
    label .go
    inds = 0
    inds2 = 0
    flagq = 1

    if flager:
        goto .keks
    txt = reverseq()

    for z in xrange(20):
        if z in ind:
            new_str+=str(smt[inds])
            inds+=1
        else:
            label .mid
            if flagq:
                start = 0
                end = len(flag1)-1
                while start < end: 
                    flag1[start], flag1[end] = flag1[end], flag1[start] 
                    start += 1
                    end -= 1
                flagq = 0
                goto .mid
            new_str += txt[inds2]
            inds2+=1
    goto .end
label .keks
a = "{"
b = "}"
def reverseq():
    global txt
    start = 0
    end = len(txt)-1
    while start < end:
        txt = list(txt)
        txt[start], txt[end] = txt[end], txt[start] 
        start += 1
        end -= 1
    return "".join(txt)
flager = 0
goto .start
label .end
print "".join(flag1)+a+new_str+b, "\n"
