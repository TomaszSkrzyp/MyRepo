import matplotlib.pyplot as plt


# Read the data from the file
data = []
current_cluster = None

with open(r"C:\Users\Dell\source\repos\232ccdd3-gr21-repo\FInalny_Projekt\liczby.txt") as file:
    for line in file:
        if line.startswith("Kluster"):
            current_cluster = int(line.split()[1])
        else:
            x, y = map(float, line.split())
            data.append((x, y, current_cluster))


clusters = {}#slownik klusterow
for x, y, cluster in data:
    if cluster not in clusters:
        clusters[cluster] = []
    clusters[cluster].append((x, y))


colors = ['red', 'green', 'blue','yellow','orange']///ilosc klustrow zalezna od ilosc klustrow
for cluster, points in clusters.items():
    x_values = [point[0] for point in points]
    y_values = [point[1] for point in points]
    plt.scatter(x_values, y_values, color=colors[cluster-1])

plt.xlabel('X')
plt.ylabel('Y')
plt.title('Cluster Plot')
plt.show()
