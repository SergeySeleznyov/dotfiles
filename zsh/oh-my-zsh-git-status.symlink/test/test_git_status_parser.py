import unittest

from git_status_parser.git_status_parser import *

class GitStatusMock:

    # https://git-scm.com/docs/git-status
    # X          Y     Meaning
    # -------------------------------------------------
    #           [MD]   not updated
    # M        [ MD]   updated in index
    # A        [ MD]   added to index
    # D         [ M]   deleted from index
    # R        [ MD]   renamed in index
    # C        [ MD]   copied in index
    # [MARC]           index and work tree matches
    # [ MARC]     M    work tree changed since index
    # [ MARC]     D    deleted in work tree
    # -------------------------------------------------
    # D           D    unmerged, both deleted
    # A           U    unmerged, added by us
    # U           D    unmerged, deleted by them
    # U           A    unmerged, added by them
    # D           U    unmerged, deleted by us
    # A           A    unmerged, both added
    # U           U    unmerged, both modified
    # -------------------------------------------------
    # ?           ?    untracked
    # !           !    ignored
    # -------------------------------------------------

    statusLineSamples = {
        " M" : " M 7",
        " D" : " D 8",
        
        "M " : "M  5",
        "MM" : "MM 6",
        "MD" : "MD 66", # TODO get real output example

        "A " : "A  21",
        "AM" : "AM 211", # TODO get real output example
        "AD" : "AD 211", # TODO get real output example

        "D " : "D  4", 
        "DM" : "DM  41", # TODO get real output example

        "R " : "R  1 -> 11",
        "RM" : "RM 2 -> 14",
        "RD" : "RD 3 -> 15",

        "C " : "C some text", # TODO get real output example
        "CM" : "CM some text", # TODO get real output example
        "CD" : "CD some text", # TODO get real output example

        "DD" : "DD some text", # TODO get real output example
        "AU" : "AU some text", # TODO get real output example
        "UD" : "UD some text", # TODO get real output example
        "UA" : "UA some text", # TODO get real output example
        "AA" : "AA some text", # TODO get real output example
                    
        "UU" : "UU 9",
        "??" : "?? 16",
        "!!" : "!! some text", # TODO get real output example
    }


    @staticmethod
    def getOuput(branchLineCode, statusLineCodes):
        output = []
        GitStatusMock.addBranchLine(output, branchLineCode)
        for statusLine in statusLineCodes:
            GitStatusMock.addLine(output, statusLine)
        output = "\n".join(output)
        return output

    @staticmethod
    def addBranchLine(output, code):
        branch_lines = {
            1: "## Initial commit on master",
            2: "## master",
            3: "## master...origin/master",
            4: "## master...origin/master [ahead 3]",
            5: "## master...origin/master [behind 2]",
            6: "## master...origin/master [ahead 3, behind 2]",
            7: "## master...origin/master [ahead 31, behind 29]",
        }
        if code in branch_lines:
            output.append(branch_lines[code])
        return output

    @staticmethod
    def addLine(output, code):
        output.append(GitStatusMock.statusLineSamples[code])

         # statusLineSamples

class Test_GitStatusMock_SelfTest(unittest.TestCase):

    def test_0(self):
        output = GitStatusMock.getOuput(0, [])
        self.assertEqual(output, "")

    def test_1(self):
        output = GitStatusMock.getOuput(1, [])
        self.assertEqual(output, "## Initial commit on master")

    def test_2(self):
        output = GitStatusMock.getOuput(1, [" M"])
        self.assertEqual(output, "## Initial commit on master\n M 7")

    def test_3(self):
        output = GitStatusMock.getOuput(2, ["AM", "UD"])
        self.assertEqual(output, "## master\nAM 211\nUD some text")

    def test_4(self):
        output = GitStatusMock.getOuput(3, ["UU", "??", "!!"])
        self.assertEqual(output, "## master...origin/master\nUU 9\n?? 16\n!! some text")

class TestGitStatusParser(unittest.TestCase):
    def check(self, response,
          localBranch="", 
          remoteBranch="", 
          ahead="", 
          behind="", 
          staged_deleted=0, 
          staged_added=0, 
          staged_modified=0, 
          unstaged_deleted=0, 
          unstaged_added=0, 
          unstaged_modified=0, 
          conflicts=0, 
          clean=False, 
          changed=False):
        self.compare(response, "localBranch", localBranch)
        self.compare(response, "remoteBranch", remoteBranch)
        self.compare(response, "ahead", ahead)
        self.compare(response, "behind", behind)
        self.compare(response, "staged_deleted", staged_deleted)
        self.compare(response, "staged_added", staged_added)
        self.compare(response, "staged_modified", staged_modified)
        self.compare(response, "unstaged_deleted", unstaged_deleted)
        self.compare(response, "unstaged_added", unstaged_added)
        self.compare(response, "unstaged_modified", unstaged_modified)
        self.compare(response, "conflicts", conflicts)
        self.compare(response, "clean", clean)
        self.compare(response, "changed", changed)

    def compare(self, response, key, value):
        self.assertEqual(response[key], value)

    def test_empty(self):
        output = GitStatusMock.getOuput(0, [])
        response = parser.parse(output)
        self.assertEqual(response, None)

    def test_wrong(self):
        output = "not a git status output"
        response = parser.parse(output)
        self.assertEqual(response, None)

    def test_branchLine1(self):
        output = GitStatusMock.getOuput(1, [])
        response = parser.parse(output)
        self.check(response, "Initial commit on master", clean=True) # TODO self.check(response, "master")

    def test_branchLine2(self):
        output = GitStatusMock.getOuput(2, [])
        response = parser.parse(output)
        self.check(response, "master", clean=True)

    def test_branchLine3(self):
        output = GitStatusMock.getOuput(3, [])
        response = parser.parse(output)
        self.check(response, "master", "origin/master", clean=True)

    def test_branchLine4(self):
        output = GitStatusMock.getOuput(4, [])
        response = parser.parse(output)
        self.check(response, "master", "origin/master", ahead='3')

    def test_branchLine5(self):
        output = GitStatusMock.getOuput(5, [])
        response = parser.parse(output)
        self.check(response, "master", "origin/master", behind='2')

    def test_branchLine6(self):
        output = GitStatusMock.getOuput(6, [])
        response = parser.parse(output)
        self.check(response, "master", "origin/master", behind='2', ahead='3')

    def test_branchLine7(self):
        output = GitStatusMock.getOuput(7, [])
        response = parser.parse(output)
        self.check(response, "master", "origin/master", behind='29', ahead='31')


    def test_statusLine__M1(self):
        output = GitStatusMock.getOuput(2, [" M"])
        response = parser.parse(output)
        self.check(response, "master", changed=True, unstaged_modified=1)

    def test_statusLine__M3(self):
        output = GitStatusMock.getOuput(2, [" M"] * 3)
        response = parser.parse(output)
        self.check(response, "master", changed=True, unstaged_modified=3)

    def test_statusLine__D4(self):
        output = GitStatusMock.getOuput(2, [" D"] * 4)
        response = parser.parse(output)
        self.check(response, "master", changed=True, unstaged_deleted=4)

    def test_statusLine_M_5(self):
        output = GitStatusMock.getOuput(2, ["M "] * 5)
        response = parser.parse(output)
        self.check(response, "master", changed=True, staged_modified=5)

    def test_statusLine_MM6(self):
        output = GitStatusMock.getOuput(2, ["MM"] * 6)
        response = parser.parse(output)
        self.check(response, "master", changed=True, staged_modified=6, unstaged_modified=6)

    def test_statusLine_MD7(self):
        output = GitStatusMock.getOuput(2, ["MD"] * 7)
        response = parser.parse(output)
        self.check(response, "master", changed=True, staged_modified=7, unstaged_deleted=7)

    def test_statusLine_A_8(self):
        output = GitStatusMock.getOuput(2, ["A "] * 8)
        response = parser.parse(output)
        self.check(response, "master", changed=True, staged_added=8)

    def test_statusLine_AM9(self):
        output = GitStatusMock.getOuput(2, ["AM"] * 9)
        response = parser.parse(output)
        self.check(response, "master", changed=True, staged_added=9, unstaged_modified=9)

    def test_statusLine_AD10(self):
        output = GitStatusMock.getOuput(2, ["AD"] * 10)
        response = parser.parse(output)
        self.check(response, "master", changed=True, staged_added=10, unstaged_deleted=10)
    
    def test_statusLine_D_11(self):
        output = GitStatusMock.getOuput(2, ["D "] * 11)
        response = parser.parse(output)
        self.check(response, "master", changed=True, staged_deleted=11)

    def test_statusLine_DM12(self):
        output = GitStatusMock.getOuput(2, ["DM"] * 12)
        response = parser.parse(output)
        self.check(response, "master", changed=True, staged_deleted=12, unstaged_modified=12)

    def test_statusLine_R_13(self):
        output = GitStatusMock.getOuput(2, ["R "] * 13)
        response = parser.parse(output)
        self.check(response, "master", changed=True, staged_modified=13)

    def test_statusLine_RM14(self):
        output = GitStatusMock.getOuput(2, ["RM"] * 14)
        response = parser.parse(output)
        self.check(response, "master", changed=True, staged_modified=14, unstaged_modified=14)

    def test_statusLine_RD15(self):
        output = GitStatusMock.getOuput(2, ["RD"] * 15)
        response = parser.parse(output)
        self.check(response, "master", changed=True, staged_modified=15, unstaged_deleted=15)
    
    # def test_statusLine_C_16(self):
    #     output = GitStatusMock.getOuput(2, ["C "] * 16)
    #     response = parser.parse(output)
    #     self.check(response, "master", changed=True, ??? )

    # def test_statusLine_CM17(self):
    #     output = GitStatusMock.getOuput(2, ["RD"] * 17)
    #     response = parser.parse(output)
    #     self.check(response, "master", changed=True, ??? )

    # def test_statusLine_CD18(self):
    #     output = GitStatusMock.getOuput(2, ["RD"] * 18)
    #     response = parser.parse(output)
    #     self.check(response, "master", changed=True, ??? )

        # "C " : "C some text", # TODO get real output example
        # "CM" : "CM some text", # TODO get real output example
        # "CD" : "RD some text", # TODO get real output example

    def test_statusLine_conflicts(self):
        conflicts = ["DD", "AU", "UD", "UA", "AA", "UU"];
        for conflict in conflicts:
            output = GitStatusMock.getOuput(2, [conflict])
            response = parser.parse(output)
            self.check(response, "master", changed=False, clean=True, conflicts=1) # not sure about changed and clean flags
                    
    def test_statusLine_untracked19(self):
        output = GitStatusMock.getOuput(2, ["??"] * 19)
        response = parser.parse(output)
        self.check(response, "master", changed=True, clean=False, unstaged_added=19)

    def test_statusLine_ignored20(self):
        output = GitStatusMock.getOuput(2, ["!!"] * 20)
        response = parser.parse(output)
        self.check(response, "master", changed=False, clean=True)

if __name__ == '__main__':
    unittest.main()