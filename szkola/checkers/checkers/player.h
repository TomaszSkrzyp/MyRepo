#pragma once
#include "moves_jumps.h"
#include "command.h"
#include <random>
class player_type {
public:
	virtual move* choose_move(std::list<move*>moves,command_control & console) = 0;
	virtual ~player_type() {}
};

class random_comp: public player_type {
	std::random_device move_choser;
public:
	move* choose_move(std::list<move*> moves, command_control& console) override;
};

class smart_computer : public player_type {


public:
	move* choose_move(std::list<move*> moves, command_control& console) override;
};

class human_player : public player_type {
public:
	move* choose_move(std::list<move*> moves, command_control& console);

};

class player {
	char color;
	std::string name;

	std::shared_ptr<player_type> p_type;
public:
	player()=default;
    	player(char c,  const std::string& player_name) :color(c), name(player_name) {
	}
	void set_type(std::shared_ptr<player_type> p_type) {
		this->p_type = p_type;
	}
	move* choose_move(std::list<move*> list, command_control& console) {

		
		console.replace_moves(list, color);
		return p_type->choose_move(list, console);
	}
	std::string get_name() {
		return name;
	}
	void set_name(std::string new_name) {
		name = new_name;
	}
};
