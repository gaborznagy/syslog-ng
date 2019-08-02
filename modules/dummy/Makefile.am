module_LTLIBRARIES          +=          \
    modules/dummy/libdummy.la

modules_dummy_libdummy_la_CFLAGS    =   \
    -I$(top_srcdir)/modules/dummy       \
    -I$(top_builddir)/modules/dummy
modules_dummy_libdummy_la_SOURCES   =   \
    modules/dummy/dummy-grammar.y       \
    modules/dummy/dummy.c               \
    modules/dummy/dummy.h               \
    modules/dummy/dummy-parser.c        \
    modules/dummy/dummy-parser.h
modules_dummy_libdummy_la_LIBADD    =   \
    $(MODULE_DEPS_LIBS)
modules_dummy_libdummy_la_LDFLAGS   =   \
    $(MODULE_LDFLAGS)
modules_dummy_libdummy_la_DEPENDENCIES  =   \
    $(MODULE_DEPS_LIBS)

modules/dummy modules/dummy/ mod-dummy: \
    modules/dummy/libdummy.la

BUILT_SOURCES               +=          \
    modules/dummy/dummy-grammar.y       \
    modules/dummy/dummy-grammar.c       \
    modules/dummy/dummy-grammar.h
EXTRA_DIST                  +=          \
    modules/dummy/dummy-grammar.ym

.PHONY: modules/dummy/ mod-dummy
