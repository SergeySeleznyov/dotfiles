#!/usr/bin/env python

from __future__ import print_function
import sys

class parser:

  ahead_token = "ahead"
  behind_token = "behind"

  @staticmethod
  def getClearResponse():
    response = {
      "localBranch": "",
      "remoteBranch": "",
      "ahead": 0,
      "behind": 0,
      "staged_deleted": 0,
      "staged_added": 0,
      "staged_modified": 0,
      "unstaged_deleted": 0,
      "unstaged_added": 0,
      "unstaged_modified": 0,
      "conflicts": 0,
      "clean": False,
      "changed": False,
    }
    return response

  @staticmethod
  def parseBranchLine(line, response):
    localBranch = ""
    remoteBranch = ""
    ahead = ''
    behind = ''

    lines = line[3:].split(' [')
    
    if len(lines) > 0:
      branches = lines[0].split('...')
      if len(branches) > 0:
        localBranch = branches[0]
      if len(branches) > 1:
        remoteBranch = branches[1]

    if len(lines) > 1:
      ahead_behind = lines[1].split("]")[0]
      aheadPos = ahead_behind.find(parser.ahead_token)
      behindPos = ahead_behind.find(parser.behind_token)

      if aheadPos != -1:
        aheadPos += len(parser.ahead_token) + 1
        ahead = ahead_behind[aheadPos:].split(",")[0]

      if behindPos != -1:
        behindPos += len(parser.behind_token) + 1
        behind = ahead_behind[behindPos:].split(",")[0]

    response["localBranch"] = localBranch
    response["remoteBranch"] = remoteBranch
    response["ahead"] = ahead
    response["behind"] = behind

    response["clean"] = True if ahead + behind == "" else False
    response["changed"] = False

  @staticmethod
  def parseStatusLines(statusLines, response):
    added     = 'A';
    deleted   = 'D';
    modified  = 'M';
    renamed   = 'R';
    untracked = '?';

    conflict  = ['DD', 'AU', 'UD', 'UA', 'DU', 'AA', 'UU']
    conflicts = 0;

    staged = {
      added     : 0,
      deleted   : 0,
      modified  : 0,
      renamed   : 0,
    }

    unstaged = {
      added     : 0,
      deleted   : 0,
      modified  : 0,
      untracked : 0,
    }

    clean = True
    changed = False

    for status_line in statusLines:

      if status_line[:2] in conflict:
        conflicts += 1
        continue

      for i, counters in zip([0, 1], [staged, unstaged]):

        key = status_line[i]
        if key and key in counters:
          counters[key] += 1
          clean = False
          changed = True

    response["staged_added"] = staged[added]
    response["staged_deleted"] = staged[deleted]
    response["staged_modified"] = staged[modified] + staged[renamed]
    response["unstaged_added"] = unstaged[added] + unstaged[untracked]
    response["unstaged_deleted"] = unstaged[deleted]
    response["unstaged_modified"] = unstaged[modified]
    response["conflicts"] = conflicts

    if not clean:
      response["clean"] = False
    if changed:
      response["changed"] = True


  @staticmethod
  def parse(output):
    if output[:2] != "##":
      return None

    response = parser.getClearResponse()

    status_lines = output.split('\n')

    parser.parseBranchLine(status_lines[0], response)

    parser.parseStatusLines(status_lines[1:], response)


    return response
