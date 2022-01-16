import re
import sys
def err():
    err = open("calc.out", "w")
    err.write("Dont Let Me Down")
    err.close()
    sys.exit()
calc=open("calc.in")

digit=["0","1","2","3","4","5","6","7","8","9"]
f1=[n1+"."+n2 for n1 in digit for n2 in digit]
tdigit=["sifir","bir","iki","uc","dort","bes","alti","yedi","sekiz","dokuz"]
f2=[n1+" "+"nokta"+" "+n2 for n1 in tdigit for n2 in tdigit]
lterm=["dogru","yanlis"]
acparan=["(","ac-parantez"]
kapaparan=[")","kapa-parantez"]
binaop=["+","-","*","arti","eksi","carpi"]
lop=["ve","veya"]
new=["nokta","olsun","degeri","Sonuc","YeniDegiskenler","AnaDegiskenler"]
keywords=digit+tdigit+lterm+acparan+kapaparan+binaop+new+lop
vardict={}
linelist=[line for line in calc]
x=0
for index in range(len(linelist)):
    if re.search("^ *AnaDegiskenler *$",linelist[index]):
        Astartindex=index
    if re.search("^ *YeniDegiskenler *$",linelist[index]):
        Ystartindex=index
    if re.search("^ *Sonuc *$",linelist[index]):
        Sstartindex=index
try:
    if Astartindex<Ystartindex<Sstartindex:
        for i in range(Astartindex):
            if re.search("^ *$",linelist[i]):
                pass
            else:
                err()
        for k in range(Astartindex+1,Ystartindex):
            if re.search("^ *$",linelist[k]):
                pass
            elif re.search("^ *([A-Za-z0-9]{1,10}) +degeri +(\d|\d\.\d|[a-z]+|[a-z]+ +nokta +[a-z]+) +olsun *$",linelist[k]):
                find=re.findall("^ *([A-Za-z0-9]{1,10}) +degeri +(\d|\d\.\d|[a-z]+|[a-z]+ +nokta +[a-z]+) +olsun *$",linelist[k])
                varname=find[0][0]
                vallist=find[0][1].split()
                value=""
                for i in vallist:
                    value+=i+" "
                value=value.rstrip()
                if value in tdigit:
                    value=digit[tdigit.index(value)]
                if value in f2:
                    value=f1[f2.index(value)]
                if varname in vardict.keys() or  varname in keywords:
                    err()
                if value in f1 or value in digit or value in tdigit or value in f2 or value in lterm:
                    vardict[varname]=value
                else:
                    err()
            else:
                err()
        for j in range(Ystartindex+1,Sstartindex):
            if re.search("^ *$", linelist[j]):
                pass
            elif re.search("^ *([A-Za-z0-9]{1,10}) +degeri +(.+) +olsun *$",linelist[j]):
                find=re.findall("^ *([A-Za-z0-9]{1,10}) +degeri +(.+) +olsun *$",linelist[j])
                varname=find[0][0]
                vallist=find[0][1].split()
                i = 0
                while vallist.count("nokta") > 0:
                    if vallist[i] == "nokta":
                        new = vallist[i - 1] + " "+"nokta"+ " " + vallist[i + 1]
                        vallist[i - 1] = new
                        vallist.pop(i + 1)
                        vallist.pop(i)
                    else:
                        i += 1
                for x in range(len(vallist)):
                    if vallist[x]=="ac-parantez":
                        vallist[x]="("
                    elif vallist[x]=="kapa-parantez":
                        vallist[x]=")"
                    elif vallist[x] in tdigit:
                        vallist[x] = digit[tdigit.index(vallist[x])]
                    elif vallist[x] == "arti":
                        vallist[x] = "+"
                    elif vallist[x] == "eksi":
                        vallist[x] = "-"
                    elif vallist[x] == "carpi":
                        vallist[x] = "*"
                    elif vallist[x] in vardict.keys():
                        vallist[x]=vardict[vallist[x]]
                    elif vallist[x] in f2:
                        vallist[x]=f1[f2.index(vallist[x])]
                a=0
                b=0
                c=1
                for e in vallist:
                    if e in vardict.keys():
                        if vardict[e] in digit or vardict[e] in tdigit or vardict[e] in f1 or vardict[e] in f2:
                            a=1
                        if vardict[e] in lterm:
                            b=1
                    else:
                        if e in digit or e in tdigit or e in f1 or e in f2 or e in binaop:
                            a=1
                        elif e in lterm or e in lop:
                            b=1
                        elif e in acparan or e in kapaparan:
                            pass
                        else:
                            c=0
                if a==1 and b==1:
                    err()
                if c==0:
                    err()
                ac=0
                ka=0
                val=0
                op=0
                vlist=[]
                olist=[]
                for m in vallist:
                    if m in acparan:
                        ac+=1
                    if m in kapaparan:
                        ka+=1
                    if m in vardict.keys() or m in digit or m in tdigit or m in f1 or m in f2 or m in lterm:
                        val+=1
                        vlist.append(m)
                    if m in binaop or m in lop:
                        op+=1
                        olist.append(m)
                if ac!=ka or val-1!=op:
                    err()
                value=""
                for t in vallist:
                    value+=t+" "
                value=value.rstrip()
                if a==1:
                    while re.search("(\d|\d\.\d) ([+*\-]) \d(\.\d|)", value):
                        value = re.sub("(\d|\d\.\d) ([+*\-]) \d(\.\d|)", "1", value)
                        while re.search("\( (\d|\d\.\d) \)", value):
                            value = re.sub("\( (\d|\d\.\d) \)", "1", value)
                    while re.search("\( (\d|\d\.\d) \)", value):
                        value = re.sub("\( (\d|\d\.\d) \)", "1", value)
                        while re.search("(\d|\d\.\d) ([+*\-]) \d(\.\d|)", value):
                            value = re.sub("(\d|\d\.\d) ([+*\-]) \d(\.\d|)", "1", value)
                    if value in f1 or value in digit:
                        if varname in vardict.keys() or varname in keywords:
                            err()
                        vardict[varname]=value
                    else:
                        err()
                if b==1:
                    while re.search("(dogru|yanlis) (ve|veya) (dogru|yanlis)",value):
                        value=re.sub("(dogru|yanlis) (ve|veya) (dogru|yanlis)","dogru",value)
                        while re.search("\( (dogru|yanlis) \)",value):
                            value=re.sub("\( (dogru|yanlis) \)","dogru",value)
                    while re.search("\( (dogru|yanlis) \)", value):
                        value = re.sub("\( (dogru|yanlis) \)", "dogru", value)
                        while re.search("(dogru|yanlis) (ve|veya) (dogru|yanlis)", value):
                            value = re.sub("(dogru|yanlis) (ve|veya) (dogru|yanlis)", "dogru", value)
                    if value in lterm:
                        if varname in vardict.keys() or varname in keywords:
                            err()
                        vardict[varname]=value
                    else:
                        err()
            else:
                err()
        check=0
        for z in range(Sstartindex+1,len(linelist)):
            if re.search("^ *$", linelist[z]):
                pass
            elif re.search("^ *(.+) *$", linelist[z]):
                find=re.findall("^ *(.+) *$",linelist[z])
                vallist = find[0].split()
                i = 0
                while vallist.count("nokta") > 0:
                    if vallist[i] == "nokta":
                        new = vallist[i - 1] + " "+"nokta"+ " " + vallist[i + 1]
                        vallist[i - 1] = new
                        vallist.pop(i + 1)
                        vallist.pop(i)
                    else:
                        i += 1
                for x in range(len(vallist)):
                    if vallist[x] == "ac-parantez":
                        vallist[x] = "("
                    elif vallist[x] == "kapa-parantez":
                        vallist[x] = ")"
                    elif vallist[x] in tdigit:
                        vallist[x] = digit[tdigit.index(vallist[x])]
                    elif vallist[x] == "arti":
                        vallist[x] = "+"
                    elif vallist[x] == "eksi":
                        vallist[x] = "-"
                    elif vallist[x] == "carpi":
                        vallist[x] = "*"
                    elif vallist[x] in vardict.keys():
                        vallist[x] = vardict[vallist[x]]
                    elif vallist[x] in f2:
                        vallist[x] = f1[f2.index(vallist[x])]
                a = 0
                b = 0
                c = 1
                for e in vallist:
                    if e in vardict.keys():
                        if vardict[e] in digit or vardict[e] in tdigit or vardict[e] in f1 or vardict[e] in f2:
                            a = 1
                        if vardict[e] in lterm:
                            b = 1
                    else:
                        if e in digit or e in tdigit or e in f1 or e in f2 or e in binaop:
                            a = 1
                        elif e in lterm or e in lop:
                            b = 1
                        elif e in acparan or e in kapaparan:
                            pass
                        else:
                            c = 0
                if a == 1 and b == 1:
                    err()
                if c == 0:
                    err()
                ac = 0
                ka = 0
                val = 0
                op = 0
                vlist = []
                olist = []
                for m in vallist:
                    if m in acparan:
                        ac += 1
                    if m in kapaparan:
                        ka += 1
                    if m in vardict.keys() or m in digit or m in tdigit or m in f1 or m in f2 or m in lterm:
                        val += 1
                        vlist.append(m)
                    if m in binaop or m in lop:
                        op += 1
                        olist.append(m)
                if ac != ka or val - 1 != op:
                    err()
                value = ""
                for k in vallist:
                    value += k+" "
                value = value.rstrip()
                if a == 1:
                    while re.search("(\d|\d\.\d) ([+*\-]) \d(\.\d|)", value):
                        value = re.sub("(\d|\d\.\d) ([+*\-]) \d(\.\d|)", "1", value)
                        while re.search("\( (\d|\d\.\d) \)", value):
                            value = re.sub("\( (\d|\d\.\d) \)", "1", value)
                    while re.search("\( (\d|\d\.\d) \)", value):
                        value = re.sub("\( (\d|\d\.\d) \)", "1", value)
                        while re.search("(\d|\d\.\d) ([+*\-]) \d(\.\d|)", value):
                            value = re.sub("(\d|\d\.\d) ([+*\-]) \d(\.\d|)", "1", value)
                    if value in f1 or value in digit:
                        pass
                    else:
                        err()
                if b == 1:
                    while re.search("(dogru|yanlis) (ve|veya) (dogru|yanlis)", value):
                        value = re.sub("(dogru|yanlis) (ve|veya) (dogru|yanlis)", "dogru", value)
                        while re.search("\( (dogru|yanlis) \)", value):
                            value = re.sub("\( (dogru|yanlis) \)", "dogru", value)
                    while re.search("\( (dogru|yanlis) \)", value):
                        value = re.sub("\( (dogru|yanlis) \)", "dogru", value)
                        while re.search("(dogru|yanlis) (ve|veya) (dogru|yanlis)", value):
                            value = re.sub("(dogru|yanlis) (ve|veya) (dogru|yanlis)", "dogru", value)
                    if value in lterm:
                        pass
                    else:
                        err()
                check+=1
            else:
                err()
        if check>1:
            err()
    else:
        err()
except:
    err()
nerr=open("calc.out","w")
nerr.write("Here Comes the Sun")
nerr.close()
