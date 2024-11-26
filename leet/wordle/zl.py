import random
with open(file="ZL.txt") as text:
    dict={}
    questions=[]
    for line in text:
        if"-" in line:
            dict[line.split("-")[0]]=line.split("-")[1]
            questions.append(line.split("-")[0])

nums=list(range(0,len(questions)))
while nums:
    index=random.choice(nums)
    word=questions[index]
    print(word)
    if input():
        print(dict[word])
        inp=input()
        if inp=="next":
                nums.remove(index)
        else:
                pass
print("coongratulations")

