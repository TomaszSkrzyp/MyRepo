#include <iostream>
void divconq(int arr[], int p, int q, int &min, int & max)
{
    if (p == q)
    {
        min = max = arr[p];
    }
    else
    {
        int midpoint = (p+q) / 2;

        int min1;
        int max1;
        int min2;
        int max2;

        divconq(arr, p, midpoint, min1,min2);
        divconq(arr, midpoint + 1, q, min2,max2);

        if (min1 < min2)
            min = min1;
        else
            min = min2;

        if (max1> max2)
            max = max1;
        else
            max = max2;
    }
}

int main()
{
    const int size = 10;
    int arr[size] = { 99, 34, 15, 17, 19, 26, 18, 783, 14, -6 };

    int min;
    int max;
    divconq(arr, 0, size - 1, min, max);
    std::cout<<min<<std::endl;
    std::cout<<max<<std::endl;
    

    return 0;
}