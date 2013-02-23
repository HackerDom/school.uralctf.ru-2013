#include <cstdio>

const char alph[] = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
void checkKey(char *key)
{
	unsigned __int64 hash = 0, mp = 1;
	for (char *c = key; *c; c++)
	{
		hash += *c * 167 * (mp *= 42);
		*c = alph[(mp ^ 16742) % 62];
	}
	if (hash == 4878096941038562048)
		printf("%s", key);
	else
		printf("You fail.");
}

int main()
{
	printf("Enter key:\n");
	char key[128];
	scanf("%s", key);
	checkKey(key);
	return 0;
}
/*
T26TH6dyVmZUDYuE
*/