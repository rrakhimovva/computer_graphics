#include <iostream>
#include <cmath>
#include <iomanip>

using namespace std;

const double EPS = 1e-9;

struct point
{
	double x, y;

	point operator+(point B)
	{
		point res;
		res.x = x + B.x;
		res.y = y + B.y;
		return res;
	}

	point operator-(point B)
	{
		point res;
		res.x = x - B.x;
		res.y = y - B.y;
		return res;
	}

	point operator*(double k)
	{
		point res;
		res.x = x * k;
		res.y = y * k;
		return res;
	}


};

int main() {

	setlocale(LC_ALL, "Russian");

	point M, N;
	double A, B, C;

	while (true)
	{
		cout << "Введите координаты точек M и N:" << endl;
		cin >> M.x >> M.y >> N.x >> N.y;
		cout << "Введите коэффициенты прямой A, B, C:" << endl;
		cin >> A >> B >> C;

		double buf_M = A * M.x + B * M.y + C;
		double buf_N = A * N.x + B * N.y + C;

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
				cout << "Обе точки лежат на прямой" << endl;
			}
			else if (fabs(buf_M) <= EPS)
			{
				cout << "Точка M лежит на прямой, точка N не лежит на прямой" << endl;
			}
			else if (fabs(buf_N) <= EPS)
			{
				cout << "Точка N лежит на прямой, точка M не лежит на прямой" << endl;
			}
		}
	}
	
}