#include"player.h"
#include <thread>
#include <chrono>        
move* random_comp::choose_move(std::list<move*> moves, command_control& console){
   
    std::mt19937 gen(move_choser());
    std::uniform_int_distribution<> dist(0, moves.size() - 1);

    int random_move_index = dist(gen);

    auto it = moves.begin();
    std::advance(it, random_move_index);

    std::this_thread::sleep_for(std::chrono::milliseconds(3000));
    return *it;
}

move* smart_computer::choose_move(std::list<move*> moves, command_control& console) {

    console.print_move();
    std::this_thread::sleep_for(std::chrono::milliseconds(2000));
    return moves.front();

}
move* human_player::choose_move(std::list<move*> moves, command_control& console) {
   /*pozniej wyrzucic*/

    console.print_move();
    return console.move_request();

}
