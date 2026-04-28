#include <iostream>
#include <cmath>

using namespace std;

const double EPS = 1e-9;

struct point
{
	double x, y, z;

	point operator+(point B)
	{
		point res;
		res.x = x + B.x;
		res.y = y + B.y;
		res.z = z + B.z;
		return res;
	}

	point operator-(point B)
	{
		point res;
		res.x = x - B.x;
		res.y = y - B.y;
		res.z = z - B.z;
		return res;
	}

	point operator*(double k)
	{
		point res;
		res.x = x * k;
		res.y = y * k;
		res.z = z * k;
		return res;
	}
};

double dot(point A, point B)
{
	return A.x * B.x + A.y * B.y + A.z * B.z;
}

point cross(point A, point B)
{
	point res;
	res.x = A.y * B.z - A.z * B.y;
	res.y = A.z * B.x - A.x * B.z;
	res.z = A.x * B.y - A.y * B.x;
	return res;
}

double mix(point v1, point v2, point normal)
{
	return dot(cross(v1, v2), normal);
}

int main()
{
	setlocale(LC_ALL, "Russian");

	point A, B, C, D;

	while (true)
	{
		cout << "Введите координаты точек A, B, C, D (x y z):\n";
		cout << "A: "; cin >> A.x >> A.y >> A.z;
		cout << "B: "; cin >> B.x >> B.y >> B.z;
		cout << "C: "; cin >> C.x >> C.y >> C.z;
		cout << "D: "; cin >> D.x >> D.y >> D.z;

		point BA = A - B;
		point BC = C - B;
		point BD = D - B;

		if (fabs(mix(BA, BC, BD)) > EPS)
		{
			cout << "Точка D не лежит в плоскости угла ABC" << endl;
		}
		else
		{
			point normal = cross(BA, BC);

			double sign1 = mix(BC, BD, normal);
			double sign2 = mix(BC, BA, normal);
			double sign3 = mix(BA, BD, normal);
			double sign4 = mix(BA, BC, normal);

			if (sign1 * sign2 >= -EPS && sign3 * sign4 >= -EPS)
			{
				cout << "Точка D лежит внутри угла ABC" << endl;
			}
			else
			{
				cout << "Точка D не лежит внутри угла ABC" << endl;
			}
		}
	}
}