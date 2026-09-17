#include <iostream>

#include "../includes/exampleLib.hpp"
#include "../includes/exampleFolder/exampleFolderLib.hpp"
#include "../includes/exampleFolder/exampleFolderInFolder/exampleFolderInFolderLib.hpp"

int main(){
    int a = 9, b = 12;

    int Sum = sum(a, b);
    int Rest = rest(b, a);
    int Mul = multiply(Sum, Rest);
    int div = 12 / 3;

    std::cout << "- a = " << a << "\n- b = " << b << "\n- a + b = " << Sum << "\n- b - a = " << Rest << "\n- (a + b) * (b - a) = " << Mul;
    std::cout << "\n" << div;

    return 0;
}
