"""setup absu package"""
import setuptools


setuptools.setup(
    name="absu",
    version="0.0.1",
    author="Jonas C. Rabe aka Quisl",
    description=(
        "This module helps updating a static website hosted by Azure Blob "
        "Storage."
    ),
    packages=["absu", "absu.modules", "absu.modules.templates"],
    install_requires=[
        "azure-storage-blob==12.13.1",  # create container and upload files
        "python-magic-bin==0.4.14",  # set Mime Types automatically
        "azure-mgmt-resource>=18.0.0",  # create resources on azure
        "azure-mgmt-subscription>=3.1.1",  # get subscription
        "azure-identity>=1.5.0",  # connect to azure
        "azure-core==1.25.1",  # for azure exceptions
    ],
)
