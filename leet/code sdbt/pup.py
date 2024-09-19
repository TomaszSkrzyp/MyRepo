lol=0
for k in range(1000,9999):
    
    lis=list(str(k))
    i=[int(num) for num in lis]
    
    if i[0]*i[3]!=0:
        if k-2997==1000*i[3]+100*i[2]+10*i[1]+i[0]:
            print(i)
            lol+=1
print(lol)