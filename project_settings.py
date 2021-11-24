import target

default_path_to_docker_file = '.'
default_docker_name = 'devenv-simple-build-system'
default_debug_port_number = '5000'

targets = {}

common_flags 			= ["-Wall",
						   "-Wextra"]
debug_flags 			= ["-g3",
						   "-O0"]
release_flags			= ["-O3"]
map_file_str			= "-Wl,-Map,{0}/{1}.map,--cref"

gdtoa_name 				= "gdtoa"
gdtoa_c_compiler 		= "gcc"
gdtoa_archiver 			= "ar"

gdtoa = target.library(
	name 				= 	gdtoa_name,
	build_dir 			= 	"build_PBS/gdtoa",
	target 				= 	"{0}.a".format(gdtoa_name),
	c_compiler 			= 	gdtoa_c_compiler,
	c_flags 			= 	common_flags,
	defines 			=	["NO_ERRNO",
							 "IFNAN_CHECK",
							 "GDTOA_NO_ASSERT",
							 "NO_FENV_H"],
	archiver 			=	gdtoa_archiver,
	archiver_flags 		= 	["rcs"],
	source_files 		= 	["src/gdtoa/src/dmisc.c",
							 "src/gdtoa/src/dtoa.c",
							 "src/gdtoa/src/g__fmt.c",
							 "src/gdtoa/src/g_ddfmt.c",
							 "src/gdtoa/src/g_dfmt.c",
							 "src/gdtoa/src/g_ffmt.c",
							 "src/gdtoa/src/g_Qfmt.c",
							 "src/gdtoa/src/g_xfmt.c",
							 "src/gdtoa/src/g_xLfmt.c",
							 "src/gdtoa/src/gdtoa.c",
							 "src/gdtoa/src/gethex.c",
							 "src/gdtoa/src/gmisc.c",
							 "src/gdtoa/src/hd_init.c",
							 "src/gdtoa/src/hexnan.c",
							 "src/gdtoa/src/misc.c",
							 "src/gdtoa/src/smisc.c",
							 "src/gdtoa/src/strtod.c",
							 "src/gdtoa/src/strtodg.c",
							 "src/gdtoa/src/strtodI.c",
							 "src/gdtoa/src/strtof.c",
							 "src/gdtoa/src/strtoId.c",
							 "src/gdtoa/src/strtoIdd.c",
							 "src/gdtoa/src/strtoIf.c",
							 "src/gdtoa/src/strtoIg.c",
							 "src/gdtoa/src/strtoIQ.c",
							 "src/gdtoa/src/strtoIx.c",
							 "src/gdtoa/src/strtoIxL.c",
							 "src/gdtoa/src/strtopd.c",
							 "src/gdtoa/src/strtopdd.c",
							 "src/gdtoa/src/strtopf.c",
							 "src/gdtoa/src/strtopQ.c",
							 "src/gdtoa/src/strtopx.c",
							 "src/gdtoa/src/strtopxL.c",
							 "src/gdtoa/src/strtord.c",
							 "src/gdtoa/src/strtordd.c",
							 "src/gdtoa/src/strtorf.c",
							 "src/gdtoa/src/strtorQ.c",
							 "src/gdtoa/src/strtorx.c",
							 "src/gdtoa/src/strtorxL.c",
							 "src/gdtoa/src/sum.c",
							 "src/gdtoa/src/ulp.c"],
	include_dirs 		= 	["src/gdtoa/include"],
	post_build_cmds 	= 	["echo Finished building {0}".format(gdtoa_name)]
)

targets[gdtoa.name] = gdtoa

# STM32F1_debug_name 		= "blinky_STM32F1_debug"
# STM32F1_debug_build_dir = "build/STM32F1/debug"
# mcu_flags 				= ["-mcpu=cortex-m3",
# 						   "-mthumb"]
# STM32f1_debugger 		=	"arm-none-eabi-gdb"
# STM32F1_debug = target.executable(
# 	name 				= 	STM32F1_debug_name,
# 	build_dir 			= 	STM32F1_debug_build_dir,
# 	target 				= 	target_str.format(STM32F1_debug_name),
# 	c_compiler 			= 	"arm-none-eabi-gcc",
# 	c_flags 			= 	common_flags + debug_flags + mcu_flags,
# 	assembler 			=	"arm-none-eabi-gcc",
# 	as_flags 			=	["-x assembler-with-cpp"] + common_flags + mcu_flags,
# 	linker 				= 	"arm-none-eabi-gcc",
# 	linker_flags 		=	linker_flags_common + \
# 							[map_file_str.format(STM32F1_debug_build_dir, STM32F1_debug_name),
# 							 "--specs=nano.specs"]
# 							 + mcu_flags,
# 	linker_script 		=	"hardware/source/STM32F1/linker-script/STM32F103C8Tx_FLASH.ld",
# 	defines 			=	["USE_HAL_DRIVER",
# 							 "STM32F103xB"],
# 	source_files 		= 	source_files_common + 
# 							["hardware/source/STM32F1/source/STM32F1.c",
# 							 "hardware/source/STM32F1/source/stm32f1xx_hal_msp.c",
# 							 "hardware/source/STM32F1/source/stm32f1xx_it.c",
# 							 "hardware/source/STM32F1/source/system_stm32f1xx.c",
# 							 "libraries/STM32CubeF1/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_gpio_ex.c",
# 							 "libraries/STM32CubeF1/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_tim.c",
# 							 "libraries/STM32CubeF1/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_tim_ex.c",
# 							 "libraries/STM32CubeF1/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal.c",
# 							 "libraries/STM32CubeF1/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_rcc.c",
# 							 "libraries/STM32CubeF1/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_rcc_ex.c",
# 							 "libraries/STM32CubeF1/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_gpio.c",
# 							 "libraries/STM32CubeF1/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_dma.c",
# 							 "libraries/STM32CubeF1/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_cortex.c",
# 							 "libraries/STM32CubeF1/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_pwr.c",
# 							 "libraries/STM32CubeF1/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_flash.c",
# 							 "libraries/STM32CubeF1/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_flash_ex.c",
# 							 "libraries/STM32CubeF1/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_exti.c",
# 							 "hardware/source/STM32F1/source/startup_stm32f103xb.s"],
# 	include_dirs 		= 	include_dirs,
# 	libraries 			= 	libraries_common + \
# 							["c", "nosys"],
# 	debugger 			=	STM32f1_debugger,
# 	post_build_cmds 	= 	["arm-none-eabi-size {0}/{1}".format(STM32F1_debug_build_dir, target_str.format(STM32F1_debug_name)),
# 							 "arm-none-eabi-objcopy -O binary -S {0}/{1} {0}/{2}.bin".format(STM32F1_debug_build_dir, target_str.format(STM32F1_debug_name), STM32F1_debug_name)]
# )

# targets[STM32F1_debug.name] = STM32F1_debug
