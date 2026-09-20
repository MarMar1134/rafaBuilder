#include <iostream>

//#include "../include/exampleHeader.hpp"

//#include "../include/exampleLib.hpp"
//#include "../include/exampleFolder/exampleFolderLib.hpp"

#include "../libs/math/include/math.hpp"
#include "../libs/math/include/point.hpp"

#include "../libs/list/include/list.hpp"

void example1(){
    int a = 9, b = 12;

    int Sum = Add(a, b);
    int Rest = Subtract(b, a);
    int Mul = Multiply(Sum, Rest);
    int div = safeDivision(12, 3);

    std::cout << "- a = " << a << "\n- b = " << b << "\n- a + b = " << Sum << "\n- b - a = " << Rest << "\n- (a + b) * (b - a) = " << Mul;
    std::cout << "\n" << div << "\n";
}

void example2(){
    Point myPoint = newPoint(0, 9);
    Point myOtherPoint = newPoint(12, 18);

    Point myPointCopy = copy(myPoint);

    Point myPointsSum = myPoint + myOtherPoint;
    Point myPointsRest = myPoint - myOtherPoint;

    std::cout << "My point{x, y}: {" << myPoint.x << "," << myPoint.y << "}\n";
    std::cout << "My other point{x, y}: {" << myOtherPoint.x << "," << myOtherPoint.y << "}\n";

    std::cout << "A copy of my point{x, y}: {" << myPointCopy.x << "," << myPointCopy.y << "}\n";

    std::cout << "Sum of my points{x, y}: {" << myPointsSum.x << "," << myPointsSum.y << "}\n";
    std::cout << "Rest of my points{x, y}: {" << myPointsRest.x << "," << myPointsRest.y << "}\n";
}

void exampleList(){
    Node* miLista = newNode(12);
    addNode(miLista, 17);
    addNode(miLista, 23);

    std::cout << "-Elementos de mi lista:\n";
    while (miLista){
        std::cout << "--" << miLista->data << "\n";
        miLista = miLista->next;
    }
}

/*void example3(){
    int a = 9, b = 12, c = 18;
    int threeSum = sumThree(a, b, c);
    int threeRest = restThree(c, b, a);

    int compoundSum = sumThree(Add(a, a), b, c);

    std::cout << "-a: " << a << "\n-b: " << b << "\n-c: " << c;
    std::cout << "\n-sum of a, b and c: " << threeSum;
    std::cout << "\n-rest of a, b and c: " << threeRest;
    std::cout << "\n-Compound sum of sum(a, a), b and c: " << compoundSum << "\n";
}*/

int main(){
    std::cout << "Example 1:\n";
    example1();

    std::cout << "Example 2:\n";
    example2();

    std::cout << "Example list:\n";
    exampleList();

    /*std::cout << "Example 3:\n";
    example3();*/

    return 0;
}
