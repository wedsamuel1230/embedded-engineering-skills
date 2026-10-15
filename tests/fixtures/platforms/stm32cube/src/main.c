#include "stm32f4xx_hal.h"
/* Compile-only HAL fixture; no peripheral/actuator configuration. */
int main(void) {
    HAL_Init();
    for (;;) { __WFI(); }
}
