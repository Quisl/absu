"""provides a container for credentials"""
from getpass import getpass
import re


def get_info_from_cli(name, hidden=False):
    """gets an information from command line"""
    if hidden:
        info = getpass(f"Enter {name}: ")
    else:
        info = input(f"Enter {name}: ")
    return info


def is_connection_string(connectionString):
    """checks if a string is a valid azure blob connection string"""
    if "AccountName" in connectionString and "AccountKey" in connectionString:
        return True
    return False


class Credentials:
    """holds the required credentials for the tool, gets data from CLI
    if they are not available"""

    def __init__(self, args):
        self.quiet = args.quiet
        try:
            self.connectionstring = args.connectionstring
        except AttributeError:
            self.connectionstring = None
        try:
            self.folder = args.folder
        except AttributeError:
            self.folder = None

        # get Connection String
        if self.connectionstring is None:
            if not self.quiet:
                self.connectionstring = get_info_from_cli(
                    name="connection string"
                )
            else:
                raise RuntimeError("No connection string")
            if not is_connection_string(self.connectionstring):
                raise ValueError("connection string is invalid!")
        self.storageName = self.get_value_from_connectionstring("AccountName")
        self.storageKey = self.get_value_from_connectionstring("AccountKey")

        # get local folder
        if self.folder is None:
            if not self.quiet:
                self.folder = get_info_from_cli(name="local folder")
            else:
                raise RuntimeError("No folder given")

    def get_value_from_connectionstring(self, value):
        """returns one of these values from the connection string:
        DefaultEndpointsProtocol, AccountName, AccountKey, EndpointSuffix"""
        return re.findall(f"{value}=([^;]+)", self.connectionstring)[0]
