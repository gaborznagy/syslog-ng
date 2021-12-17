#!/usr/bin/env python
#############################################################################
# Copyright (c) 2021 One Identity
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published
# by the Free Software Foundation, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
# As an additional exemption you are allowed to compile & link against the
# OpenSSL libraries as published by the OpenSSL project. See the file
# COPYING for details.
#
#############################################################################

def test_file_destination_symlink_as(config, syslog_ng):
    generator_source = config.create_example_msg_generator_source(num=1, template=config.stringify("test message text"))
    file_destination = config.create_file_destination(file_name=r'output-${ISODATE}.log', symlink_as=config.stringify('/tmp/latest.log'))
    config.create_logpath(statements=[generator_source, file_destination])

    syslog_ng.start(config)
    assert file_destination.read_until_logs(["test message text"])
