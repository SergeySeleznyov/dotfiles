#!/usr/bin/env python

from __future__ import print_function
import sys
from git_status_parser.git_status_parser import *

git_status_output = sys.stdin.read();

if git_status_output[:2] != "##":
  sys.exit(0)

response = parser.parse(git_status_output)

output = ' '.join([
  response["localBranch"],
  response["remoteBranch"],
  response["ahead"],
  response["behind"],
  str(response["staged_deleted"]),
  str(response["staged_added"]),
  str(response["staged_modified"]),
  str(response["unstaged_deleted"]),
  str(response["unstaged_added"]),
  str(response["unstaged_modified"]),
  str(response["conflicts"]),
  str(response["clean"]),
  str(response["changed"]),
  ])
print(output, end='')