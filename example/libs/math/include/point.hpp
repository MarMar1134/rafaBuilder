#ifndef POINT_HPP
#define POINT_HPP

struct Point {
    int x;
    int y;

    Point operator+(Point point){
        return Point{x + point.x, y + point.y};
    }

    Point operator-(Point point){
        return Point{x - point.x, y - point.y};
    }
};

Point newPoint(int x, int y);
Point copy(Point point);


#endif