#include <iostream>

#include "../include/math.h"

int Add(int a, int b){
    return a + b;
}

int Subtract(int a, int b){
    return a - b;
}

int Multiply(int a, int b){
    return a * b;
}

int safeDivision(int a, int b){
    if (b == 0){
        std::cout << "Can't divide by 0";
        return -1;
    }

    return a / b;
}