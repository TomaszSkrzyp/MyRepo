#include <iostream>
int findMax(int arr[], int start, int end) {
    if (start == end) {
        return arr[start];
    }
    int mid = (start + end) / 2;
    int leftMax = findMax(arr, start, mid);
    int rightMax = findMax(arr, mid + 1, end);
     
     if (leftMax > rightMax) {
        return leftMax;
    }
    else {
        return rightMax;
    }
}
int main(){
    int arr[10] = { 99, 34, 15, 17, 19, 26, 18, 783, 14, -6 };
    int max = findMax(arr, 0, 9);
    std::cout<<max<<std::endl;
    return 0;
}
