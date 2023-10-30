import turtle as t
t.speed(10)
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
        t.rt(112.5)
        trojkat(size/1.5,level-1)#pierwsza galez
        for i in range(5):
            
            t.lt(45)
            trojkat(size/1.5,level-1)#galezie 2-6
       

        t.rt(112.5)
        t.forward(-size)


trojkat(300,4)

t.time.sleep(5)
