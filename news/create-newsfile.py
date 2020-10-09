#!/usr/bin/env python3
#############################################################################
# Copyright (c) 2020 Balabit
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

import re
import sys
from argparse import ArgumentParser
from pathlib import Path
from subprocess import PIPE, Popen

news_dir = Path(__file__).resolve().parent
root_dir = news_dir.parent
newsfile = root_dir / 'NEWS.md'

last_version = None
next_version = None

team_members = [
    "Andras Mitzki",
    "Antal Nemes",
    "Attila Szakacs",
    "Balazs Scheidler",
    "Gabor Nagy",
    "Laszlo Budai",
    "Laszlo Szemere",
    "László Várady",
    "Norbert Takacs",
    "Zoltan Pallagi",
]


def print_usage_if_needed():
    ArgumentParser(usage="\rCreates NEWS.md file from the entries in the news/ folder.\n"
                         "It also deletes the entry files.").parse_args()


def _exec(command):
    proc = Popen(command, cwd=str(root_dir), stdout=PIPE, shell=True)
    stdout, _ = proc.communicate()
    stdout = stdout.decode()
    return stdout


def create_block(block_name, files):
    block = '## {}\n\n'.format(block_name)
    for f in files:
        entry = ''
        try:
            pr_id = re.findall(r'\d+.md$', f.name)[0][:-3]
        except IndexError:
            sys.exit('Invalid filename: {}'.format(f.name))
        entry += ' * {}\n([#{}](https://github.com/syslog-ng/syslog-ng/pull/{}))'.format(f.read_text().rstrip(), pr_id, pr_id)
        entry = entry.replace('\n', '\n   ')
        block += entry + '\n'
    block += '\n'
    return block


def get_last_version():
    stdout = _exec(r'git show HEAD:NEWS.md')
    return stdout[:stdout.index('\n')]


def create_version():
    global next_version, last_version

    next_version = (root_dir / 'VERSION').read_text().rstrip()
    last_version = get_last_version()

    if next_version == last_version:
        print('VERSION file contains the same version as the current NEWS.md file.\n'
              'Probably you are trying to create the newsfile before bumping the `VERSION` file.\n'
              'Please provide version to be released.')
        next_version = input('Version to be released: ')

    return '{}\n{}\n\n'.format(next_version, len(next_version) * '=')


def create_highlights_block():
    return '## Highlights\n' \
           '\n' \
           '<Fill this block manually from the blocks below>\n' \
           '\n'


def create_standard_blocks():
    standard_blocks = ''
    blocks = [
        ('Features', 'feature-*.md'),
        ('Bugfixes', 'bugfix-*.md'),
        ('Packaging', 'packaging-*.md'),
        ('Notes to developers', 'developer-note-*.md'),
        ('Other changes', 'other-*.md'),
    ]
    for block_name, glob in blocks:
        entries = list(news_dir.glob(glob))
        if len(entries) > 0:
            standard_blocks += create_block(block_name, entries)
    return standard_blocks


def create_credits_block():
    def join_with_length_limit(contributors):
        limit = 70
        lines = ['']

        for contributor in contributors:
            buffer = lines[-1]
            buffer += ' ' + contributor + ','
            if len(buffer) > limit:
                lines.append(contributor + ',')
            else:
                lines[-1] = buffer

        return '\n'.join(lines)[1:-1]

    stdout = _exec(r'git rev-list --no-merges --format=format:%an syslog-ng-' + last_version + r'..HEAD | '
                   r'grep -Ev "^commit [a-z0-9]{40}$" | sort | uniq')
    contributors = stdout.rstrip().split('\n')
    contributors += team_members
    contributors = sorted(list(set(contributors)))

    return '## Credits\n' \
           '\n' \
           'syslog-ng is developed as a community project, and as such it relies\n' \
           'on volunteers, to do the work necessarily to produce syslog-ng.\n' \
           '\n' \
           'Reporting bugs, testing changes, writing code or simply providing\n' \
           'feedback are all important contributions, so please if you are a user\n' \
           'of syslog-ng, contribute.\n' \
           '\n' \
           'We would like to thank the following people for their contribution:\n' \
           '\n' \
           '{}\n'.format(join_with_length_limit(contributors))


def create_newsfile(news):
    newsfile.write_text(news)
    print('Newsfile created at {}\n'.format(newsfile.resolve()))


def cleanup():
    print("Cleaning up entry files with `git rm news/*-*.md`:")
    _exec("git rm news/*-*.md")


def create_news_content():
    news = create_version()
    news += create_highlights_block()
    news += create_standard_blocks()
    news += create_credits_block()
    return news


def main():
    print_usage_if_needed()
    news = create_news_content()
    create_newsfile(news)
    cleanup()


if __name__ == '__main__':
    main()
