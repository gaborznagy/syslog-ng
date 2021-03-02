#!/usr/bin/env python
#############################################################################
# Copyright (c) 2015-2021 Balabit
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


def test_internal_source_with_threaded_destination(config, syslog_ng):
    internal_source = config.create_internal_source()
    example_destination = config.create_example_destination(filename="output.txt")
    config.create_logpath(statements=[internal_source, example_destination])

    syslog_ng.start(config, stderr=False, debug=True, trace=False, verbose=False)
    assert example_destination.wait_file_content("syslog-ng starting up")

    for _ in range(0, 5):
        syslog_ng.reload(config)
        assert example_destination.wait_file_content("Configuration reload finished")

    syslog_ng.stop()
    assert example_destination.wait_file_content("syslog-ng shutting down")