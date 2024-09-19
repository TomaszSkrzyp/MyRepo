#pragma once
#include<list>
#include<iostream>
class jump{
	char j_piece;
	jump* prev;
	bool next;
	int key = 0;
	/*przeskoczone piony*/
	char jumped;
	int xj;
	int yj;
	/*start i finish*/
	int xs;
	int ys;

	int xf;
	int yf;
public:

	int n_jump;
	jump(char j_p, char j, int x_j, int y_j, int x_s, int y_s, int x_f, int y_f, jump* p, int k) : prev(p), j_piece(j_p), jumped(j), xj(x_j), yj(y_j), n_jump(0), next(false), xs(x_s), ys(y_s), xf(x_f), yf(y_f), key(k) {
		
	}
	
	int get_key()const { return key; }
	jump* get_prev() { return prev; }
	 void set_next(bool new_next) { next = new_next; }
	bool get_next() const { return next; }
	char get_piece() const { return j_piece; }
	char get_jumped_piece() const { return jumped; }
	int get_xs()const { return xs; }
	int get_ys() const { return ys; }
	int get_xf()const { return xf; }
	int get_yf() const{ return yf; }

	 int get_xj() const{ return xj; }
	 int get_yj() const{ return yj; }


};
class move {

	char piece;
	/*start*/
	int xs;
	int ys;
	/*finisz*/
	int xf;
	int yf;
	
	
public:

	move(char p, int x_s, int y_s, int x_f, int y_f) : piece(p), xs(x_s), ys(y_s), xf(x_f), yf(y_f) {
		
	}
	std::list<jump*> jumps;
	move(move& copied):piece(copied.get_piece()), xs(copied.get_xs()), ys(copied.get_ys()), xf(copied.get_xf()), yf(copied.get_yf()) {
		for (std::list<jump*>::iterator it = copied.jumps.begin(); it != copied.jumps.end(); ++it)
		{
			
			jump* copied_jump = new jump(*(*it));
			jumps.push_back(copied_jump);
		}

	}
	~move() {
		for (std::list<jump*>::iterator it = jumps.begin(); it != jumps.end(); ++it)
		{
			--(*it)->n_jump;
			if ((*it)->n_jump == 0) {
				delete (*it);
			}
		}
	}
	
	bool has_kinging_occured(char piece_after);
	/*getters*/
	int get_xs() const { return xs; }
	int get_ys() const { return ys; }
	int get_xf() const{ return xf; }
	 int get_yf() const { return yf; }
	char get_piece() const{ return piece; }
	void set_start(int x, int y) {
		xs = x;
		ys = y;
	}
	void set_finish(int x, int y) {
		xf = x;
		yf = y;
	}
	/*sprawdzanie czy nalezy "ukoronowac" piona*/
	const void print_jumps();


};