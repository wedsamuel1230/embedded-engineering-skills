#include <zephyr/kernel.h>
/* Compile-only scheduler fixture; no I/O. */
int main(void) {
    for (;;) { k_sleep(K_SECONDS(1)); }
    return 0;
}
