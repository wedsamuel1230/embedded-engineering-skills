#include "pico/stdlib.h"
/* Compile-only SDK fixture; no GPIO or actuator initialization. */
int main(void) { for (;;) { tight_loop_contents(); } }
