#include <iostream>

using namespace std;

struct node
{
    int data;
    node *next;
};

class linked_list
{
private:
    node *head,*tail;
public:
    linked_list()
    {
        head = NULL;
        tail = NULL;
    }

    void add_node(int n)
    {
        node *tmp = new node;
        tmp->data = n;
        tmp->next = NULL;

        if(head == NULL)
        {
            head = tmp;
            tail = tmp;
        }
        else
        {
            tail->next = tmp;
            tail = tail->next;
        }
    }

    node* gethead()
    {
        return head;
    }
    node *getthird()
    {
        return head->next->next;
    }

    static void display(node *head)
    {
        if(head == NULL)
        {
            cout << "NULL" << endl;
        }
        else
        {
            cout << head->data << endl;
            display(head->next);
        }
    }

    static void concatenate(node *a,node *b)
    {
        if( a != NULL && b!= NULL )
        {
            if (a->next == NULL)
                a->next = b;
            else
                concatenate(a->next,b);
        }
        else
        {
            cout << "Either a or b is NULL\n";
        }
    }
    void front(int n){
        node *tmp=new node;
        tmp->data=n;
        tmp->next=head;
        head=tmp;

    }
    void insert(node *a,int n){
        node *p=new node;
        p->data=n;
        p->next=a->next;
        a->next=p;
    }
    node *nodegiver(linked_list a,int which){
        node *cur;
        cur=a.gethead();
        for(int i=0;i<which-1;i++){
            cur=cur->next;
        }
        return cur;
    }

        
    
};

int main()
{
    linked_list a;
    a.add_node(1);
    a.add_node(2);
    a.add_node(3);
    linked_list b;
    b.add_node(4);
    b.add_node(5);
    b.add_node(6);
    linked_list::concatenate(a.gethead(),b.gethead());
    
    
    a.insert(a.nodegiver(a,1),44);
    
    
    a.display(a.gethead());
    int h;
    cin>>h;
    return 0;
}