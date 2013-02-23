#include <cstdio>

bool calculate(__int64 a, __int64 b, char op, __int64 &result)
{
	switch (op)
	{
	case '+':
		result = a + b;
		return true;;
	case '-':
		result =  a - b;
		return true;
	case '*':
		result = a * b;
		return true;
	case '/':
		if (b == 0)
			result = a ^ 0x1bab;
		else
			result = a / b;
		return true;
	default:
		return false;
	}
}

__int64 readNumber()
{
	__int64 number = 0, mp = 1, result = 0;
	while (true)
	{		
		char c = getchar();
		if (c >= '0' && c <= '9')
		{
			number += (c - '0') * mp;
			mp *= 10;
		}
		else if (c != ' ' && c != '\t')
		{
			if (c != '\n')
				ungetc(c, stdin);
			break;
		}
	}
	mp /= 10;
	for (__int64 oldmp = mp; mp > 0; mp /= 10)
		result = result + number / mp * (oldmp / mp), number %= mp;
	return result;
}
char readChar()
{
	while (true)
	{		
		char c = getchar();
		if (c != ' ' && c != '\t')
		{
			return c;
		}
	}
}

int main()
{
	__int64 a, b, result;
	char op;
	printf("Enter an expression (^\\s*\\d+\\s*[+-*/]\\s*\\d+\\s*$):\n");
	a = readNumber(), op = readChar(), b = readNumber();
	if (calculate(a, b, op, result))
	{
		printf("%lld\n", result);
	}
	else
	{
		printf("Unsupported operation '%c'\n", op);
		return 1;
	}
	return 0;
}
