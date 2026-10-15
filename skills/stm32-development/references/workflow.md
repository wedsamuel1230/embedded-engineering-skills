# STM32 build and peripheral diagnosis

The fixture uses `nucleo_f401re`, PlatformIO `ststm32@19.5.0` and the resolved
STM32Cube F4 framework. It calls HAL initialization and idles; it does not
configure motor outputs or validate the carrier/clock physically.

For CMake use the repository's configure/build presets and record the Arm GCC
and Ninja/CMake versions. Preserve compiler CPU/FPU/float ABI, CMSIS device
macro, startup assembly and the exact linker map. Cube-generated Make projects
remain Make projects unless migration is requested.

Before a HAL transfer, inspect the generated MSP initialization, GPIO alternate
function, clock gate, NVIC handler and DMA channel/request selection. For a
callback that never fires, verify the IRQ handler forwards to the correct HAL
handle and the interrupt is enabled; do not guess a universal DMA mapping.
Cache maintenance/alignment matters on cache-enabled MCUs and differs from
F401. Read that part's reference manual; do not generalize an M7 workaround.

Primary sources: [ST CMake AN5952](https://www.st.com/resource/en/application_note/an5952-how-to-use-cmake-in-stm32cubeide-stmicroelectronics.pdf),
[CubeCLT UM3088](https://www.st.com/resource/en/user_manual/um3088-stm32cube-commandline-toolset-quick-start-guide-stmicroelectronics.pdf),
[STM32CubeF4](https://github.com/STMicroelectronics/STM32CubeF4),
[STM32CubeProgrammer](https://www.st.com/en/development-tools/stm32cubeprog.html).
