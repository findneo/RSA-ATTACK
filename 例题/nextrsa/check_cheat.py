import os


ips=os.listdir("cheat")
cheatlist=[]
for ip in ips:
    f=open("./cheat/"+ip).readlines()
    ind=0
    while ind<len(f):
        if "token" in f[ind]:
            token = f[ind].split(":")[1].strip()
            time=int(f[ind+1].split(":")[1].strip(),10)
            d = f[ind+3].split(":")[1].strip().replace("L","")
            n = f[ind + 4].split(":")[1].strip().replace("L","")
            cheatlist.append((token,time,d,n))
        ind+=1

ips=os.listdir("success")
successlist=[]
for ip in ips:
    f=open("./success/"+ip).readlines()
    ind=0
    while ind<len(f):
        if "token" in f[ind]:
            token = f[ind].split(":")[1].strip()
            time=int(f[ind+1].split(":")[1].strip(),10)
            d = f[ind+3].split(":")[1].strip().replace("L","")
            n = f[ind + 4].split(":")[1].strip().replace("L","")
            successlist.append((token,time,d,n))
        ind+=1

for i in cheatlist:
    (cheat_token,cheat_time,cheat_d,cheat_n)=i
    find_father=0
    for j in successlist:
        (token,time,d,n)=j
        if token==cheat_token and cheat_d==d and cheat_n==n and cheat_time>time:
            find_father=1
            break
    if find_father==0:
        print cheat_token
        for j in successlist:
            (token, time, d, n) = j
            if cheat_d==d and cheat_n==n and cheat_time>time:
                print "from",token