import target

default_path_to_docker_file = 'Python-Build-System-with-Ninja'
default_docker_name = 'devenv-simple-build-system'
default_debug_port_number = '5000'

targets = {}

target_str 				= "{0}.elf"
common_flags 			= ["-std=c11",
						   "-Wall",
						   "-ffunction-sections",
						   "-fdata-sections"]
debug_flags 			= ["-g3",
						   "-O0"]
release_flags			= ["-O3"]
include_dirs 			= ["include",
						   "hardware/include",
						   "hardware/source/STM32F1/include",
						   "libraries/STM32CubeF1/STM32F1xx_HAL_Driver/Inc",
						   "libraries/STM32CubeF1/STM32F1xx_HAL_Driver/Inc/Legacy",
						   "libraries/STM32CubeF1/CMSIS/Device/ST/STM32F1xx/Include",
						   "libraries/STM32CubeF1/CMSIS/Include",
						   "libraries/STM32CubeF1/CMSIS/Include"]
source_files_common		= ["source/main.c"]
linker_flags_common		= ["-Wl,--gc-sections"]
libraries_common 		= ["m"]
map_file_str			= "-Wl,-Map,{0}/{1}.map,--cref"

x86_name 				= "blinky_x86"
x86_build_dir 			= "build/x86"
x86_source_files 		=  source_files_common + \
						  ["hardware/source/x86/x86.c"]
x86_c_compiler 			= "gcc"
x86_linker 				= "gcc"
x86_debugger 			= "gdb"

x86_debug_name 			= x86_name + "_debug"
x86_debug_build_dir 	= x86_build_dir + "/debug"
x86_debug = target.executable(
	name 				= 	x86_debug_name,
	build_dir 			= 	x86_debug_build_dir,
	target 				= 	target_str.format(x86_debug_name),
	c_compiler 			= 	x86_c_compiler,
	c_flags 			= 	common_flags + debug_flags,
	linker 				= 	x86_linker,
	linker_flags 		=	linker_flags_common + \
							[map_file_str.format(x86_debug_build_dir, x86_debug_name)],
	source_files 		= 	x86_source_files,
	include_dirs 		= 	include_dirs,
	libraries 			= 	libraries_common,
	debugger 			=	x86_debugger,
	post_build_cmds 	= ["echo Finished building {0}".format(x86_debug_name)]
)

targets[x86_debug.name] = x86_debug

x86_release_name 		= x86_name + "_release"
x86_release_build_dir 	= x86_build_dir + "/release"
x86_release = target.executable(
	name 				= 	x86_release_name,
	build_dir 			= 	x86_release_build_dir,
	target 				= 	target_str.format(x86_release_name),
	c_compiler 			= 	x86_c_compiler,
	c_flags 			= 	common_flags + release_flags,
	linker 				= 	x86_linker,
	linker_flags 		=	linker_flags_common + \
							[map_file_str.format(x86_release_build_dir, x86_release_name)],
	source_files 		= 	x86_source_files,
	include_dirs 		= 	include_dirs,
	libraries 			= 	libraries_common,
	debugger 			=	x86_debugger,
	post_build_cmds 	= ["echo Finished building {0}".format(x86_release_name)]
)

targets[x86_release.name] = x86_release

STM32F1_debug_name 		= "blinky_STM32F1_debug"
STM32F1_debug_build_dir = "build/STM32F1/debug"
mcu_flags 				= ["-mcpu=cortex-m3",
						   "-mthumb"]
STM32f1_debugger 		=	"arm-none-eabi-gdb"
STM32F1_debug = target.executable(
	name 				= 	STM32F1_debug_name,
	build_dir 			= 	STM32F1_debug_build_dir,
	target 				= 	target_str.format(STM32F1_debug_name),
	c_compiler 			= 	"arm-none-eabi-gcc",
	c_flags 			= 	common_flags + debug_flags + mcu_flags,
	assembler 			=	"arm-none-eabi-gcc",
	as_flags 			=	["-x assembler-with-cpp"] + common_flags + mcu_flags,
	linker 				= 	"arm-none-eabi-gcc",
	linker_flags 		=	linker_flags_common + \
							[map_file_str.format(STM32F1_debug_build_dir, STM32F1_debug_name),
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
	libraries 			= 	libraries_common + \
							["c", "nosys"],
	debugger 			=	STM32f1_debugger,
	post_build_cmds 	= 	["arm-none-eabi-size {0}/{1}".format(STM32F1_debug_build_dir, target_str.format(STM32F1_debug_name)),
							 "arm-none-eabi-objcopy -O binary -S {0}/{1} {0}/{2}.bin".format(STM32F1_debug_build_dir, target_str.format(STM32F1_debug_name), STM32F1_debug_name)]
)

targets[STM32F1_debug.name] = STM32F1_debug
