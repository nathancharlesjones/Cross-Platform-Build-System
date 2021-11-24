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

libc_name 				= "c"
libc_c_compiler 		= "gcc"
libc_archiver 			= "ar"
libc_source_files_assert	= ["src/assert/assert.c"]
libc_source_files_ctype		= ["src/ctype/isalnum.c",
							   "src/ctype/isalpha.c",
							   "src/ctype/isascii.c",
							   "src/ctype/isblank.c",
							   "src/ctype/iscntrl.c",
							   "src/ctype/isdigit.c",
							   "src/ctype/isgraph.c",
							   "src/ctype/islower.c",
							   "src/ctype/isprint.c",
							   "src/ctype/ispunct.c",
							   "src/ctype/isspace.c",
							   "src/ctype/isupper.c",
							   "src/ctype/isxdigit.c",
							   "src/ctype/toascii.c",
							   "src/ctype/tolower.c",
							   "src/ctype/toupper.c"]
libc_source_files_locale	= ["src/locale/langinfo.c"]
libc_source_files_math		= ["math/fabs.c",
    						   "math/fabsf.c"]
libc_source_files_stdio		= ["src/stdio/asprintf.c",
    						   "src/stdio/putchar.c",
    						   "src/stdio/puts.c",
    						   "src/stdio/vasprintf.c"]
libc_source_files_stdio_native	= ["src/stdio/putchar_native.c"]
libc_source_files_stdlib	= ["src/stdlib/abs.c",
							   "src/stdlib/atof.c",
							   "src/stdlib/atoi.c",
							   "src/stdlib/atol.c",
							   "src/stdlib/atoll.c",
							   "src/stdlib/bsearch.c",
							   "src/stdlib/calloc.c",
							   "src/stdlib/div.c",
							   "src/stdlib/heapsort_r.c",
							   "src/stdlib/heapsort.c",
							   "src/stdlib/imaxabs.c",
							   "src/stdlib/imaxdiv.c",
							   "src/stdlib/labs.c",
							   "src/stdlib/ldiv.c",
							   "src/stdlib/llabs.c",
							   "src/stdlib/lldiv.c",
							   "src/stdlib/qsort_r.c",
							   "src/stdlib/qsort.c",
							   "src/stdlib/rand.c",
							   "src/stdlib/realloc.c",
							   "src/stdlib/strtol.c",
							   "src/stdlib/strtold.c",
							   "src/stdlib/strtoul.c",
							   "src/stdlib/strtoll.c",
							   "src/stdlib/strtoull.c"]
libc_source_files_string	= ["src/string/memcmp.c",
    						   "src/string/memcpy.c",
    						   "src/string/memmem.c",
    						   "src/string/memmove.c",
    						   "src/string/memchr.c",
    						   "src/string/memrchr.c",
    						   "src/string/memset.c",
    						   "src/string/strcat.c",
    						   "src/string/strchr.c",
    						   "src/string/strchrnul.c",
    						   "src/string/strcmp.c",
    						   "src/string/strcoll.c",
    						   "src/string/strcpy.c",
    						   "src/string/strcspn.c",
    						   "src/string/strdup.c",
    						   "src/string/strerror.c",
    						   "src/string/strerror_r.c",
    						   "src/string/strlen.c",
    						   "src/string/strncat.c",
    						   "src/string/strncmp.c",
    						   "src/string/strncpy.c",
    						   "src/string/strndup.c",
    						   "src/string/strnlen.c",
    						   "src/string/strnstr.c",
    						   "src/string/strpbrk.c",
    						   "src/string/strrchr.c",
    						   "src/string/strspn.c",
    						   "src/string/strstr.c",
    						   "src/string/strtok.c",
    						   "src/string/strxfrm.c"]
libc_source_files_support	= ["src/support/fls.c",
    						   "src/support/flsl.c",
    						   "src/support/flsll.c"]
libc_source_files_time		= ["src/time/asctime.c",
    						   "src/time/asctime_r.c"]
libc_source_files_wchar		= ["src/wchar/iswalnum.c",
							   "src/wchar/iswalpha.c",
							   "src/wchar/iswblank.c",
							   "src/wchar/iswcntrl.c",
							   "src/wchar/iswctype.c",
							   "src/wchar/iswdigit.c",
							   "src/wchar/iswgraph.c",
							   "src/wchar/iswlower.c",
							   "src/wchar/iswprint.c",
							   "src/wchar/iswpunct.c",
							   "src/wchar/iswspace.c",
							   "src/wchar/iswupper.c",
							   "src/wchar/iswxdigit.c",
							   "src/wchar/towccase.c",
							   "src/wchar/towctrans.c",
							   "src/wchar/towlower.c",
							   "src/wchar/towupper.c",
							   "src/wchar/wcswidth.c",
							   "src/wchar/wctrans.c",
							   "src/wchar/wctype.c",
							   "src/wchar/wcwidth.c"]

libc = target.library(
	name 				= 	libc_name,
	build_dir 			= 	"build_PBS/c",
	target 				= 	"{0}.a".format(libc_name),
	c_compiler 			= 	libc_c_compiler,
	c_flags 			= 	common_flags,
	archiver 			=	libc_archiver,
	archiver_flags 		= 	["rcs"],
	source_files 		= 	#libc_source_files_assert + \
							libc_source_files_ctype + \
							libc_source_files_locale + \
							#libc_source_files_math + \
							#libc_source_files_stdio	+ \
							#libc_source_files_stdio_native + \
							libc_source_files_stdlib + \
							libc_source_files_string + \
							libc_source_files_support + \
							#libc_source_files_time + \
							libc_source_files_wchar,
	include_dirs 		= 	["include",
							 "arch/x86_64/include"],
	post_build_cmds 	= 	["echo Finished building {0}".format(libc_name)]
)

targets[libc.name] = libc