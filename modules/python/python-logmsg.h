/*
 * Copyright (c) 2015 Balabit
 * Copyright (c) 2015 Balazs Scheidler <balazs.scheidler@balabit.com>
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
 *
 * As an additional exemption you are allowed to compile & link against the
 * OpenSSL libraries as published by the OpenSSL project. See the file
 * COPYING for details.
 *
 */

#ifndef _SNG_PYTHON_LOGMSG_H
#define _SNG_PYTHON_LOGMSG_H

#include "python-module.h"

typedef struct _PyLogMessage
{
  PyObject_HEAD
  LogMessage *msg;
  PyObject *bookmark_data;
  gboolean cast_to_strings;
} PyLogMessage;

extern PyTypeObject py_log_message_type;

int py_is_log_message(PyObject *obj);
PyObject *py_log_message_new(LogMessage *msg);

void py_log_message_global_init(void);


#endif
