#include <cstdio>
#include <cstring>

const char alph[] = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
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
		checkKey(newKey);
	else if (hash == 17455650878452034834)
		printf("Key:{%s}", key);
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
L7qEgPZeAXt5m8Eq
*/