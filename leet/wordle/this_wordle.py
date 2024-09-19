import random
import string
import time
def wordle():
    letter_dict={}
    words={}
    letters=list(string.ascii_lowercase)
    
    
    with open('wordle/words.txt','r') as f:
        for line in f:
            line=line.strip("\n")
            words[line]=1
            for k in set(line):
                if k not in letter_dict:
                   letter_dict[k]=1
                else:
                  letter_dict[k]+=1
        for letter in letter_dict.keys():
                letter_dict[letter]=round(letter_dict[letter],3)
    word=random.choice(list(words.keys()))
    
    modify(words,letter_dict)
    for i in range(6):
        if len(words.keys())==0:
            return 6
        maxi=max(words,key=words.get)
        new_green={}
        new_yellow={}
        new_black={}
        #print("guess word: "+maxi)
        #print(len(words))
        #print("give input")
        #x=get_input()
        x=checker(word,maxi)
        if x=="ggggg":
            print("word is: "+maxi+ " found in: "+str(i)+" attempts")
            return i
        for i,v in enumerate(x):
            if v=="b":
                if maxi[i] not in  new_black:
                    new_black[maxi[i]]=[i]
                else:
                    new_black[maxi[i]].append(i)
            elif v=="y":
                if maxi[i] not in  new_yellow:
                    new_yellow[maxi[i]]=[i]
                else:
                    new_yellow[maxi[i]].append(i)
            elif v=="g":
                if maxi[i] not in  new_green:
                    new_green[maxi[i]]=[i]
                else:
                    new_green[maxi[i]].append(i)      
        poke(new_green,new_black,new_yellow,words)
        if len(words)==0:
            print("removed")
            return 6
    print(words.keys(),word)
    if word in words.keys():
        print("word was: "+word+ " and you have not found it loser")
        return 6
    else:
        print("word was: "+word+ " and you have not found it loser")
        print("also, you removed it")
        return 6
def get_input():
    x=input()
    if len(x)==5:
        for i in x:
            if i not in ["b","g","y"]:
                 print("wrong input")
                 return get_input()   
        return x
    else:
        print("wrong input")
        return get_input()    
def modify(words,letter_dict):
    
    for line in words.keys():
            n=1
            for k in set(line):
                    n*=(1-letter_dict[k]/12500)
            words[line]=round(1-n,5)
def poke(green,black,yellow,words):
    
    words_to_remove=[]
    for word in words.keys():
        if(b_poke(black,green,word) or 
            g_poke(green,word) or
            y_poke(yellow,word)  ):
            words_to_remove.append(word)
            
    for w in words_to_remove:
        words.pop(w)
    
    
def b_poke(black,green,word):
    for index,letter in enumerate(word):
        if letter in black.keys():
            if letter in green.keys():
                if (index) in black[letter]:
                    return True
            else:
                return True
def y_poke(yellow,word):
    for y in yellow.keys():
        if y not in word:
            return True
        else:
            for index,letter in enumerate(word):
                if letter==y:
                    if index in yellow[y]:
                        return True

def g_poke(green,word):
    for g in green.keys():
        if g not in word:
            return True
        else:
            for index in green[g]:
                if word[index]!=g:
                    return True
    
def checker(word,guess):
    s=""
    for i,v in enumerate(guess):
        if v in list(word):
            if word[i]==v:
                s+="g"
            else:
                s+="y"
        else:
            s+="b"
    return s

def test(n):
    sum=0
    time_sum=0
    for i in range(n):
        clk1=time.time()
        sum+=wordle() 
        time_sum+=time.time()-clk1
    print("average score: "+str(sum/n)+" in average time: "+str(time_sum/n))    
test(1000)
    


