"""provides connectors for Azure Blob"""
import os
import logging
from azure.storage.blob import BlobServiceClient, ContentSettings
import magic


def _query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer."""
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError(f"invalid default answer: '{default}'")
    while True:
        print(question + prompt)
        choice = input().lower()
        if default is not None and choice == "":
            return valid[default]
        if choice in valid:
            return valid[choice]
        print("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")


class AzureBlobConnector:
    """Handles Azure Blob Storage communication"""

    def __init__(self, creds):
        self.container = "$web"
        self.creds = creds
        self.bsc = BlobServiceClient.from_connection_string(
            self.creds.connectionstring
        )
        self.containerClient = self.bsc.get_container_client(
            container=self.container
        )

    def create_container(self):
        """makes sure the container exists. True if didn't exist else False"""
        returnvalue = False
        containers = []
        for container in self.bsc.list_containers():
            containers.append(container["name"])
        if self.container not in containers:
            self.bsc.create_container(self.container, public_access="BLOB")
            returnvalue = True
        return returnvalue

    def clean_container(self):
        """deletes files in container"""
        if self.quiet:
            for i in self.containerClient.list_blobs():
                self.containerClient.delete_blob(blob=i["name"])
        if _query_yes_no(
            f"Delete all files in the container {self.container}"
        ):
            for i in self.containerClient.list_blobs():
                self.containerClient.delete_blob(blob=i["name"])
        else:
            raise SystemExit("User exited")

    def upload_folder(self):
        """uploads the folder to the container"""
        for root, _, files in os.walk(self.creds.folder):
            for name in files:
                dir_part = os.path.relpath(root, self.creds.folder)
                dir_part = "" if dir_part == "." else dir_part + "/"
                file_path = os.path.join(root, name)
                blob_path = dir_part + name
                self.upload_file(file_path, blob_path)

    def upload_file(self, source, dest):
        """Upload a single file to a path inside the container"""
        logging.info("Uploading %s to %s", source, dest)
        mime = magic.Magic(mime=True)
        with open(source, "rb") as data:
            if ".css" in source[-4:]:
                mimetype = ContentSettings(content_type="text/css")
            else:
                mimetype = ContentSettings(content_type=mime.from_file(source))
            self.containerClient.upload_blob(
                name=dest, data=data, content_settings=mimetype
            )
