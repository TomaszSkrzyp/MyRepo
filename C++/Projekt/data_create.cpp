#include<fstream>
#include<iostream>
#include<string>
#include<vector>
#include<random>
void vec(std::vector<int>& vector,int size){
    static std::default_random_engine re{ std::random_device{}() };
    using Dist = std::uniform_int_distribution<int>;
    static Dist uid{};
    for (int i = 0; i < size; i++){
        vector.push_back(uid(re, Dist::param_type{ 0,100 }));   
    }
}
template <size_t n, size_t k>
void create_table_of_objects(int(&table)[n][k]){{
		std::ifstream get_data("dataset.txt");
		if (get_data){
			int liczba;
            int i=0;
			while (get_data >> liczba){
                table[(int)i/k][(int)i%k]=liczba;
                std::cout<<i/k<<" ";
                i+=1;
			}
		}
	
	}
}

        


int main(){
    constexpr int k=3;
    constexpr int ile_pkt=20;
    std::vector<int> data;
    vec(data,k*ile_pkt);
    std::ofstream dataset;
    dataset.open("dataset.txt");
    if(dataset)
    for(int i=0;i<(int)k*ile_pkt;i++){
        dataset<<data[i]<<"\n";}
        /*if (i%k==k-1 && i!=0){
            dataset<<"\n";
        }
    }*/
    dataset.close();
    int table[ile_pkt][k];
    create_table_of_objects(table);
    for(int i=0;i<ile_pkt;i++){
        for(int l=0;l<k;l++){
            std::cout<<table[i][l]<<" ";
        }
        std::cout<<std::endl;
    }
    return 0;   
}
    