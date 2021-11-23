# In-development, alternate means of defining targets that allows a target to be defined
# as the combination of other objects (e.g. the target "x86_debug" is composed on line 55
# of "all_common", "x86_common", and "debug_build". Not pursued, because although 
# this form of definition feels more compact and maximizes code reuse, I felt that it
# might actually be harder to use and/or introduce more errors, since it would not be
# immediately apparent (on line 55, for instance) whether or not all of the various properties
# of each target were completely or correctly defined.

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
