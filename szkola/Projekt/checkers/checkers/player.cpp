#include"player.h"
#include <thread>
#include <chrono>        
move* random_comp::choose_move(std::list<move*> moves, command_control& console){
   
    std::mt19937 gen(move_choser());
    std::uniform_int_distribution<> dist(0, moves.size() - 1);

    int random_move_index = dist(gen);

    auto it = moves.begin();
    std::advance(it, random_move_index);
    /*do wyrzucenia*/
    return *it;
}

move* smart_computer::choose_move(std::list<move*> moves, command_control& console) {
    return moves.front();

}
