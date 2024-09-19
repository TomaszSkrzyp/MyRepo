#include <string>
#include <iostream>
using namespace std;

    int find_end(string s, int index){
            
            for(int i=index;i<s.size();i++){
                if(int(s[i])>57 || int(s[i])<47){
                    return i-1;
                }
            }
            return s.size()-1;
    }
    int res(string word, int start,int end){
        int r=0;
        for(int i=start;i<=end;i++){
            r+=int(word[i]-48)*pow(10,end-i);
            
        }
        return r;
    }
  
    int myAtoi(string s) {
        int wynik=0;
        int end;
        for(int i=0;i<s.size();i++){
            if(int(s[i]==32)){
                continue;
            }
            if(int(s[i]==45)){
                
                end=find_end(s,i+1);
                
                if(i+1==end){
                    return 0;
                }
                return -res(s,i+1,end);
            }
            else{if (int(s[i])<58 && int(s[i])>47){
                
                end=find_end(s,i);
                if(i==end){
                    return 0;
                }
                return res(s,i,end);
            }
            }
            return 0;
            

        }

        return 0;
    }

int main(){
    string x="-1";
    while(1){
        x.append('1',1);
        if(myAtoi(x)>0){
            cout<<x;
            break;
        }
        cout<<x;

    }
}