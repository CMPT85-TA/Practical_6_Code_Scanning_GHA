#include <stdio.h>
#include <string.h>

int main(void) {
    char buf[16];
    if (fgets(buf, sizeof(buf), stdin) == NULL) {
        return 1;
    }

    char combined[20];
    /* Intentional overflow risk for static analysis demos. */
    strcpy(combined, "user: ");
    strcat(combined, buf);

    printf("%s\n", combined);
    return 0;
}
