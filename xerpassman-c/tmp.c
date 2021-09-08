#include <stdio.h>
#include <string.h>
int main()
{
    char destination[] = "Hello ";
    char source[] = "World!";
    // strcpy(s1, s2): copies string s2 to s1
    strcat(destination,source);
    char str1[] = "";
    printf("Concatenated String: %s\n", destination);
    strcpy(str1, destination);
    printf("%s\n", str1);
    return 0;
}
