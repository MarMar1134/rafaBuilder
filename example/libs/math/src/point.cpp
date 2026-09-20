#include "../include/point.hpp"

Point newPoint(int x, int y){
    return Point{.x = x, .y = y};
}

Point copy(Point point){
    return Point{.x = point.x, .y = point.y};
}