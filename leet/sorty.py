def bubble(x):
  
    comps=0
    for i in range(0,len(x)):
        for j in range(1,len(x)):
            comps+=1
            print("comparing"+str(x[j-1])+str(x[j]))
            if x[j-1]>x[j]:
                temp=x[j]
                x[j]=x[j-1]
                x[j-1]=temp
                print("swaping"+str(x[j-1])+str(x[j]))
                swaps+=1
    print(swaps,comps)
def wybieranie(x):
    comps=0
    for i in range(0,len(x)-1):
        indeks_min=i
        wartosc_min=x[i]
        for j in range(i+1, len(x)):
            comps+=1
            print("comparing"+str(x[j])+str(wartosc_min))
            if x[j]<wartosc_min:
                wartosc_min=x[j]
                indeks_min=j
        
        
        x[indeks_min]=x[i]
        x[i]=wartosc_min
        print("najmniejsza od indeksu"+str(i)+"jest"+str(wartosc_min))
       
    print(comps)   
def wstawianie(x):

    comps=0 
    for i in range(1,len(x)):
        wartosc_min=x[i]
        j=i-1
        while j>-1 and wartosc_min<x[j]:
            comps+=1
            print("swaping"+str(x[j+1])+str(x[j]))
            x[j+1]=x[j]
            j=j-1
        print("zmienianie wartosci"+str(x[j+1])+"na"+str(wartosc_min))
        x[j+1]=wartosc_min
    print(x)
    return x
def partition(array, low, high):
 
    # choose the rightmost element as pivot
    pivot = array[high]
 
    # pointer for greater element
    i = low - 1
 
    # traverse through all elements
    # compare each element with pivot
    for j in range(low, high):
        if array[j] <= pivot:
 
            # If element smaller than pivot is found
            # swap it with the greater element pointed by i
            i = i + 1
 
            # Swapping element at i with element at j
            (array[i], array[j]) = (array[j], array[i])
 
    # Swap the pivot element with the greater element specified by i
    (array[i + 1], array[high]) = (array[high], array[i + 1])
 
    # Return the position from where partition is done
    return i + 1
 
# function to perform quicksort
 
 
def quickSort(array, low, high):
    if low < high:
 
        # Find pivot element such that
        # element smaller than pivot are on the left
        # element greater than pivot are on the right
        pi = partition(array, low, high)
 
        # Recursive call on the left of pivot
        quickSort(array, low, pi - 1)
 
        # Recursive call on the right of pivot
        quickSort(array, pi + 1, high)
 
 
data = [1, 7, 4, 1, 10, 9, -2]
print("Unsorted Array")
print(data)
 
size = len(data)
 
quickSort(data, 0, size - 1)