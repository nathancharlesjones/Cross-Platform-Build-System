import target
from helper import mergesum

default_path_to_docker_file = 'Python-Build-System-with-Ninja'
default_docker_name = 'devenv-simple-build-system'
default_debug_port_number = '5000'

targets = {}

def add_common_settings(target):
	common_build_dir = "build_PBS"
	common = 	{
					"build_dir"		: 	common_build_dir + "/" + target["name"],
					"c_flags"		: [	"all",
							   			"extra"]
				}
	return mergesum(target, common)

gdtoa = {}
gdtoa["name"]				= 	"gdtoa"
gdtoa = add_common_settings(gdtoa)
gdtoa["target_type"]		= 	"library" # Can I just check target for .a?
gdtoa["target"]				= 	"{0}.a".format(gdtoa["name"])
gdtoa["c_compiler"]			= 	"gcc"
gdtoa["defines"]			= [	"NO_ERRNO",
								"IFNAN_CHECK",
								"GDTOA_NO_ASSERT",
								"NO_FENV_H"]
gdtoa["archiver"]			= 	"gcc-ar"
gdtoa["archiver_flags"]		= [	"rcs"]
gdtoa["source_files"]		= [ "src/gdtoa/src/dmisc.c",
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
								"src/gdtoa/src/ulp.c"]
gdtoa["include_dirs"] 		= [	"src/gdtoa/include"]
gdtoa["post_build_cmds"]	= [	"echo Finished building {0}".format(gdtoa["name"])]

targets[gdtoa["name"]] = gdtoa


libc = {}
libc["name"] 				= 	"c"
libc = add_common_settings(libc)
libc["target_type"]			= 	"library" # Can I just check target for .a?
libc["target"]				= 	"{0}.a".format(libc["name"])
libc["c_compiler"]			=	"gcc"
libc["archiver"]			= 	"gcc-ar"
libc["archiver_flags"]		= [	"rcs"]

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

libc["source_files"]		= []
libc["source_files"] 		+= 	libc_source_files_assert
libc["source_files"] 		+= 	libc_source_files_ctype
libc["source_files"] 		+= 	libc_source_files_locale
#libc["source_files"] 		+= 	libc_source_files_math
#libc["source_files"] 		+= 	libc_source_files_stdio
#libc["source_files"] 		+= 	libc_source_files_stdio_native
libc["source_files"] 		+= 	libc_source_files_stdlib
libc["source_files"] 		+= 	libc_source_files_string
libc["source_files"] 		+= 	libc_source_files_support
#libc["source_files"] 		+= 	libc_source_files_time
libc["source_files"] 		+= 	libc_source_files_wchar

libc["include_dirs"] 		= 	["include",
								 "arch/x86_64/include"]
libc["post_build_cmds"] 	= 	["echo Finished building {0}".format(libc["name"])]

targets[libc["name"]] = libc