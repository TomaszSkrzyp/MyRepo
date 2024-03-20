import matplotlib.pyplot as plt
data=[]
with open(r"C:\Users\Dell\source\repos\232ccdd3-gr21-repo\FInalny_Projekt\dataset.txt") as file:
    for line in file:
        x,y=map(float,line.split())
        data.append((x,y))
    for point in data:
        plt.scatter(point[0],point[1])
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Cluster Plot')
plt.show()

