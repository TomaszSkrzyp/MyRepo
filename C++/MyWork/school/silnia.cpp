#include <iostream>
using namespace std;
int silnia(int n){
    if (n<2){
        return 1;
    }
    else{
        return n*silnia(n-1);
   }
    }
int main(){
    int liczba;
    cout<<"jaka liczba?";
    cin>>liczba;
    cout<<silnia(liczba);
    return 0;
}
