#ifndef DUMMY_H_INCLUDED
#define DUMMY_H_INCLUDED

#include "driver.h"

LogDriver *dummy_dd_new(GlobalConfig *cfg);

void dummy_dd_set_filename(LogDriver *d, const gchar *filename);

#endif
