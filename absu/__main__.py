"""executable part of the module"""
import logging
from absu.modules.parameterparser import get_parameters
from absu.modules.credentials import Credentials
from absu.modules.azureblobconnector import AzureBlobConnector
from absu.modules.azureconnector import AzureConnector


if __name__ == "__main__":
    logging.info("Getting parameters from parameters...")
    args = get_parameters()
    logging.info("Ok.")
    if args.verbose:
        logging.root.setLevel(logging.NOTSET)
    if not args.connectionstring:
        logging.info("No connection string given, connecting to Azure...")
        ac = AzureConnector()
        logging.info("Ok.")
        if not args.storage:
            args.storage = input("Azure Blob Storage account name: ")
        logging.info("Creating/updating resource group...")
        ac.create_resource_group(args.resourcegroup)
        logging.info("Ok.")
        logging.info("Creating/updating storage...")
        while not ac.create_storage_account(args.resourcegroup, args.storage):
            ac.storage = input("Could not create storage, try another name: ")
        logging.info("Ok.")
        logging.info("Downloading connection string...")
        args.connectionstring = ac.get_connection_string(
            args.storage, args.resourcegroup
        )
        logging.info("Ok.")
    logging.info("Checking foldername + connection string credentials...")
    cred = Credentials(args)
    logging.info("Ok.")
    logging.info("Connecting to storage...")
    abc = AzureBlobConnector(cred)
    logging.info("Ok.")
    logging.info("Creating container on storage...")
    abc.create_container()  # if doesnt exist
    logging.info("Ok.")
    logging.info("Deleting all files in container...")
    abc.clean_container()  # if files exist
    logging.info("Ok.")
    logging.info("Uploading folder to storage...")
    abc.upload_folder()  # files in folder
