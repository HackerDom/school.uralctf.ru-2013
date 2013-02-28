#include <cstdio>
#include <cstring>

const char alph[] = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";

void checkKey2(char *key);
void checkKey(char *key)
{
	if (strlen(key) != 16)
	{
		printf("You fail.\n");
		return;
	}
	char *newKey = new char[strlen(key)];
	strcpy(newKey, key);
	unsigned __int64 hash = 0, mp = 1;
	for (char *c = newKey; *c; c++)
	{
		hash += *c * 0xdead * (mp *= 0xface);
		*c = alph[(mp ^ 0xdeadface) % 62];
	}
	if (hash == 12046408001372443516)
		checkKey2(key);
	else
		printf("You fail.\n");
}

void checkKey2(char *key)
{
	unsigned __int64 hash = 0, mp = 1;
	for (char *c = key; *c; c++)
	{
		hash += *c * 0xface * (mp *= 0xdead);
		*c = alph[(mp ^ 0xfacedead) % 62];
	}
	if (hash == 5398040367137414880)
		printf("Key:{%s}", key);
	else
		printf("You fail.\n");
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
L7qEgPZeAXt5m8Eq
*/