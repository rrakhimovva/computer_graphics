#include <iostream>
#include <cmath>
#include <iomanip>

using namespace std;

const double EPS = 1e-9;

struct point
{
	double x, y;

	point operator-(point B)
	{
		point res;
		res.x = x - B.x;
		res.y = y - B.y;
		return res;
	}

    bool operator==(point B)
    {
        bool res = false;
        if (this->x == B.x && this->y == B.y)
        {
            res = true;
        }
        return res;
    }
};

double dist2(point A)
{
	return (A.x * A.x + A.y * A.y);
}

double dot(point A, point B)
{
	return A.x * B.x + A.y * B.y;
}


int main() {

	setlocale(LC_ALL, "Russian");

	point A, B, C, D;

    while (true)
    {
        cout << "Введите координаты точек A, B, C, D:" << endl;
        cout << "A: "; cin >> A.x >> A.y;
        cout << "B: "; cin >> B.x >> B.y;
        cout << "C: "; cin >> C.x >> C.y;
        cout << "D: "; cin >> D.x >> D.y;

        // Векторы направлений лучей
        point AB = B - A;
        point CD = D - C;

        // Вектор от начала первого луча к началу второго
        point AC = C - A;
        point CA = A - C;

        double dot_AB_CD = dot(AB, CD);
        double dot_AC_AB = dot(AC, AB);

        if (dot_AB_CD > 0)
        {
            if (A == C)
            {
                cout << "Лучи совпадают" << endl;
            }
            else
            {
                cout << "Лучи пересекаются" << endl;
            }
        }
        else
        {
            if (dot_AC_AB >= -EPS)
            {
                cout << "Лучи пересекаются" << endl;
            }
            else
            {
                cout << "Лучи не пересекаются" << endl;
            }
        }
    }
}