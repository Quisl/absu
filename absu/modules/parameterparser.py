"""provides a function that parses the command line parameters"""
import argparse


def get_parameters():
    """parses the parameters from command line"""
    parser = argparse.ArgumentParser(
        description="Please provide at least one of the following: "
        "1) a Azure Blob Storage name OR 2) a connection string. "
    )
    parser.add_argument(
        "-c",
        "--connectionstring",
        help="Azure Blob Storage connection string.",
    )
    parser.add_argument(
        "-s",
        "--storage",
        help="Azure Blob Storage resource name. Creates new one if not existing.",
    )
    parser.add_argument(
        "-r",
        "--resourcegroup",
        help="The Azure Blob Storage is in this resource group. Default: blogs-rg",
        default="blogs-rg",
    )
    parser.add_argument(
        "-f",
        "--folder",
        help="Folder with static website data. Will be pushed to the storage.",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        help="Run this tool in silent mode / quiet mode.",
        action="store_true",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Verbose, use this flag for debugging.",
        action="store_true",
    )
    return parser.parse_args()
