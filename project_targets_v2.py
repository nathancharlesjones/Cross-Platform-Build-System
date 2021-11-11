import target

targets = {}

all_common = target.target(
	c_flags 			= ["-std=c11",
						   "-Wall",
						   "-ffunction-sections",
						   "-fdata-sections"],
	linker 				=  "gcc",
	linker_flags 		= ["-Wl,--gc-sections,-Map,{0}/{1}.map,--cref".format(x86_debug_build_dir, x86_debug_name)],
	include_dirs 		= ["include",
						   "hardware/include",
						   "hardware/source/STM32F1/include",
						   "libraries/STM32CubeF1/STM32F1xx_HAL_Driver/Inc",
						   "libraries/STM32CubeF1/STM32F1xx_HAL_Driver/Inc/Legacy",
						   "libraries/STM32CubeF1/CMSIS/Device/ST/STM32F1xx/Include",
						   "libraries/STM32CubeF1/CMSIS/Include",
						   "libraries/STM32CubeF1/CMSIS/Include"],
	source_files 		= ["source/main.c"],
	libraries 			= ["m"]
)

debug_build = target.target(
	name 				=  "_debug",
	build_dir 			=  "/debug",
	target 				=  "{0}.elf".format(STM32F1_debug_name),
	c_flags				= ["-g3",
						   "-O0"]
)

release_build = target.target(
	name 				=  "_release",
	build_dir 			=  "/release",
	target 				=  "{0}.elf".format(STM32F1_debug_name),
	c_flags				= ["-O3"]
)

x86_common = target.target(
	name 				=  "blinky_x86",
	build_dir 			=  "build/x86",
	c_compiler 			=  "gcc",
	source_files 		= ["hardware/source/x86/x86.c"],
	linker 				=  "gcc"
)

x86_debug = target.executable([all_common, x86_common, debug_build])
targets[x86_debug.name] = x86_debug

x86_release = target.executable([all_common, x86_common, release_build])
targets[x86_release.name] = x86_release

STM32F1_common = target.target(
	name 				=  "blinky_STM32F1",
	build_dir 			=  "build/STM32F1",
	c_compiler 			=  "arm-none-eabi-gcc",
	c_flags 			= ["-mcpu=cortex-m3",
			 			   "-mthumb"],
	assembler 			=  "arm-none-eabi-gcc",
	as_flags 			= ["-x assembler-with-cpp"]
)

STM32F1_debug_name = "blinky_STM32F1_debug"
STM32F1_debug_build_dir = "build/STM32F1/debug"
STM32F1_debug_target = "{0}.elf".format(STM32F1_debug_name)
mcu_flags = ["-mcpu=cortex-m3",
			 "-mthumb"]
STM32F1_debug = target.executable(
	name 				= 	STM32F1_debug_name,
	build_dir 			= 	STM32F1_debug_build_dir,
	target 				= 	STM32F1_debug_target,
	c_compiler 			= 	"arm-none-eabi-gcc",
	c_flags 			= 	common_flags + debug_flags + mcu_flags,
	assembler 			=	"arm-none-eabi-gcc",
	as_flags 			=	["-x assembler-with-cpp"] + common_flags + mcu_flags,
	linker 				= 	"arm-none-eabi-gcc",
	linker_flags 		=	["-Wl,--gc-sections,-Map,{0}/{1}.map,--cref".format(STM32F1_debug_build_dir, STM32F1_debug_name),
							 "--specs=nano.specs"]
							 + mcu_flags,
	linker_script 		=	"hardware/source/STM32F1/linker-script/STM32F103C8Tx_FLASH.ld",
	defines 			=	["USE_HAL_DRIVER",
							 "STM32F103xB"],
	source_files 		= 	source_files_common + 
							["hardware/source/STM32F1/source/STM32F1.c",
							 "hardware/source/STM32F1/source/stm32f1xx_hal_msp.c",
							 "hardware/source/STM32F1/source/stm32f1xx_it.c",
							 "hardware/source/STM32F1/source/system_stm32f1xx.c",
							 "libraries/STM32CubeF1/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_gpio_ex.c",
							 "libraries/STM32CubeF1/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_tim.c",
							 "libraries/STM32CubeF1/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_tim_ex.c",
							 "libraries/STM32CubeF1/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal.c",
							 "libraries/STM32CubeF1/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_rcc.c",
							 "libraries/STM32CubeF1/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_rcc_ex.c",
							 "libraries/STM32CubeF1/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_gpio.c",
							 "libraries/STM32CubeF1/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_dma.c",
							 "libraries/STM32CubeF1/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_cortex.c",
							 "libraries/STM32CubeF1/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_pwr.c",
							 "libraries/STM32CubeF1/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_flash.c",
							 "libraries/STM32CubeF1/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_flash_ex.c",
							 "libraries/STM32CubeF1/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_exti.c",
							 "hardware/source/STM32F1/source/startup_stm32f103xb.s"],
	include_dirs 		= 	include_dirs,
	libraries 			= 	["m", "c", "nosys"],
	post_build_cmds 	= 	["arm-none-eabi-size {0}/{1}".format(STM32F1_debug_build_dir, STM32F1_debug_target),
							 "arm-none-eabi-objcopy -O binary -S {0}/{1} {0}/{2}.bin".format(STM32F1_debug_build_dir, STM32F1_debug_target, STM32F1_debug_name)]
)

targets[STM32F1_debug.name] = STM32F1_debug
