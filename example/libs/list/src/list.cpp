#include "../include/list.hpp"

Node* newNode(int data){
    Node* aux = new Node();

    aux->data = data;
    aux->next = nullptr;

    return aux;
}

void addNode(Node* self, int data){
    Node* aux = new Node();
    aux->data = data;
    aux->next = nullptr;

    if (!self){
        self = aux;
        return;
    } else {
        Node* current = self;

        while (current->next != nullptr){
            current = current->next;

            current->next = aux;
        }
    }    
}