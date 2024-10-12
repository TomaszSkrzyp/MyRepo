#include <iostream>
#include <random>
template<class T>
class Node {
public:
	T data;
	std::shared_ptr<Node> Next;

	Node(T value) : data(value), Next(nullptr) {}
	
};
template<class T>
class Queue {
private:
	int size;
	std::shared_ptr<Node<T>> front;
public:
	Queue(){
		front = nullptr;
		size = 0;
	}
	void JoinQueue(T new_data) {
		std::shared_ptr<Node<T>> new_node = std::make_shared<Node<T>>(new_data);
		if (front == nullptr) {
			front = new_node;
		}
		else{
			std::shared_ptr<Node<T>> cur_node = front;
			while (cur_node->Next != nullptr) {
				cur_node = cur_node->Next;
			}
		cur_node->Next = new_node;
	}	
		size += 1;
		std::cout << "Added value" << new_data << " ";
	}
	std::shared_ptr<Node<T>> Pop() {
		if (front == nullptr) {
			std::cout << "Queue is empty, cannot pop\n";
			return nullptr;
		}
		std::shared_ptr<Node<T>> queue_top = front;
		front = front->Next;
		size -= 1;
		std::cout << "popped value " << queue_top->data << " ";
		return front;
	}
	void fill_n_values(int n) {
		std::random_device dev;
		std::uniform_int_distribution<int> randint(1, 10000);
		for (int i=0; i < n; i++) {
			JoinQueue(randint(dev));

		}
	}



};

int main() {
	Queue <double> queue;
	queue.fill_n_values(100);

	queue.JoinQueue(17);

	queue.JoinQueue(82);
	for (int i=0; i < 100; i++) {
		std::cout << queue.Pop()->data;
	}


}