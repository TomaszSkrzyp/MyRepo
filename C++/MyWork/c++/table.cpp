#include <iostream>
using namespace std;

int main(){
    int k;
    int w;
    cout<<"podaj rozmiar swojego zygzaka";
    cin>>k;
    cin>>w;
    int table[k][w];
    for(int i=0;i<k;i++){
        if (i%2==0){
        for (int e=0;e<w;e++){
            table[i][e]=i*w+e;
        }}
        else{
            for (int e=w;e>0;e=e-1){
            table[i][e-1]=i*w+(w-e);
            cout<<i*w+(w-e);
        }
      }
    }
    for(int i=0;i<k;i++){
        for(int e=0;e<w;e++){
            cout<<table[i][e]<<" ";
        }
        cout<<endl;
    }
    return 0;
    
}