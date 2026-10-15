#include <cstdio>
// Compile fixture only. No device/peripheral mutation or OTA is performed.
extern "C" void app_main() { std::puts("native build fixture"); }
