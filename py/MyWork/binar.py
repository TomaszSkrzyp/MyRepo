import turtle as t
t.speed('fastest')

# możliwe ruchy zółwia
# t.forward(side)
# t.back(side)
# t.left
# t.right

#ustawienie początkowej pozycji żółwia
t.color('blue')
def turtle(size,level):
    if level>0:
        for i in range(3):
            turtle(size/2,level-1)
            t.forward(size)
            t.lt(120)
turtle(1000,10)
t.time.sleep(5)