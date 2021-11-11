import target

targets = {}

libtest_name = "libtest"
libtest_build_dir = "build/" + libtest_name
libtest_target = libtest_name + ".a"

libtest = target.library(
	name 				= 	libtest_name,
	c_compiler 			= 	"gcc",
	archiver 			= 	"ar",
	archiver_flags 		= 	['rcs'],
	build_dir 			= 	libtest_build_dir,
	target 				= 	libtest_target,
	source_files 		= 	["lib/test/src/test_func.c"],
	include_dirs 		= 	["lib/test/inc"],
	pre_build_cmds 		= 	["echo Beginning build for " + libtest_name],
	post_build_cmds 	= 	["echo Finished building " + libtest_name]
)

targets[libtest.name] = libtest

hello_world_name = "hello_world"
hello_world_build_dir = "build/" + hello_world_name
hello_world_target = hello_world_name + ".exe"

hello_world = target.executable(
	name 				= 	hello_world_name,
	c_compiler 			= 	'gcc',
	c_flags 			= 	['-g3','-O0'],
	linker 				= 	'gcc',
	build_dir 			= 	hello_world_build_dir,
	target 				= 	hello_world_target,
	source_files 		= 	['src/main.c'],
	include_dirs 		= 	["lib/test/inc"],
	libraries 			= 	["test", "m"],
	library_dirs 		= 	[libtest_build_dir],
	local_dependencies 	= 	[libtest],
	pre_build_cmds 		= 	["echo Beginning build for " + hello_world_name],
	post_build_cmds 	= 	["echo Finished building " + hello_world_name,
							 "./{0}/{1}".format(hello_world_build_dir, hello_world_target)]
)

targets[hello_world.name] = hello_world
