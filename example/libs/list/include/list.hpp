#ifndef LIB_LIST_HPP
#define LIB_LIST_HPP

struct Node {
    int data;
    Node* next;
};

Node* newNode(int data);
void addNode(Node* self, int data);

#endif