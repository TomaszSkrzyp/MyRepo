import turtle as t
t.speed('fastest')
t.penup()
t.rt(90)
t.forward(400)
t.lt(180)
t.pendown()
def trojkat(size,level):
    if level>0:
        t.colormode(255)
        t.pencolor(0, 255//level, 0) 
          
        
        t.forward(size)
        t.rt(45)
        trojkat(size/1.5,level-1)
        t.lt(90)
        trojkat(size/1.5,level-1)
        t.pencolor(0, 255//level, 0) 
        t.rt(45)
        t.forward(-size)


trojkat(300,12)

t.time.sleep(5)
