#include <iostream>
#include <vector>
int main(){
    std::vector<int> vec={8,5,2};
    
         std::cout << vec.capacity();
         vec=vec/2;
         std::cout << vec.capacity();

    
    return 0;
}