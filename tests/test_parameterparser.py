from unittest.mock import patch
import sys
import absu.modules.parameterparser


def test_parameterparser():
    """test absu.modules.parameterparser.get_parameters()
    checking if all testvalues are available with testcli"""
    testcli = (
        "python -c cstring -s storage -r resourcegroup " "-f folder -q -v"
    ).split()
    with patch.object(sys, "argv", testcli):
        args = absu.modules.parameterparser.get_parameters()
    testvalues = [
        "connectionstring",
        "storage",
        "resourcegroup",
        "folder",
        "quiet",
        "verbose",
    ]
    assert all(value in args for value in testvalues)
