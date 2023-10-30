import turtle as t
t.speed(5)
t.penup()
t.rt(90)
t.forward(100)
t.lt(90)
t.pendown()

def trojkat(size,level):
    if level>0:
        t.colormode(255)
        t.pencolor(0, 255//level, 0) 
          
        for i in range(2):
            t.forward(size)
            t.rt(90)
            t.forward(1/4*size)
            t.lt(90)
            trojkat(size/2,level-1)
            t.rt(90)
            t.forward(3/4*size)
            t.rt(90)
        
        



trojkat(150,4)
print(150/(2)^4)

t.time.sleep(5)
