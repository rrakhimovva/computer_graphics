#include <iostream>
#include <cmath>
#include <iomanip>

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


int main() {

	setlocale(LC_ALL, "Russian");

	point M, N;
	double A, B, C, D;

	while (true)
	{
		cout << "Введите координаты точек M и N (x y z):" << endl;
		cin >> M.x >> M.y >> M.z >> N.x >> N.y >> N.z;
		cout << "Введите коэффициенты плоскости A, B, C, D:" << endl;
		cin >> A >> B >> C >> D;

		double buf_M = A * M.x + B * M.y + C * M.z + D;
		double buf_N = A * N.x + B * N.y + C * N.z + D;

		if (buf_M * buf_N > EPS)
		{
			cout << "По одну сторону" << endl;
		}
		else if (buf_M * buf_N < -EPS)
		{
			cout << "По разные стороны" << endl;
		}
		else
		{
			if (fabs(buf_M) <= EPS && fabs(buf_N) <= EPS)
			{
				cout << "Обе точки лежат на плоскости" << endl;
			}
			else if (fabs(buf_M) <= EPS)
			{
				cout << "Точка M лежит на плоскости, точка N не лежит на плоскости" << endl;
			}
			else if (fabs(buf_N) <= EPS)
			{
				cout << "Точка N лежит на плоскости, точка M не лежит на плоскости" << endl;
			}
		}
	}
}