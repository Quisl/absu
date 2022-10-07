# *absu*: Azure Blob Storage Updater

## What is it?

*absu* is a tool that helps you manage a local folder with static files. This is useful if you want to host a website that you generated with a static website generator like [hugo](https://gohugo.io/), [mkdocs](https://www.mkdocs.org/), [Jekyll](https://jekyllrb.com/), [next.js](https://nextjs.org/) and so on...

*absu* does the following things:

* create a resource group in Azure
* create a Storage Account within that resource group
* create a container within that storage
* delete all files in that container
* upload all data from a local folder into that container

You can skip the first two steps by providing a connection string to an existing Azure Blob Storage.

## How to install

If you want the tool to create the Azure Blob storage, you will need to have:
* [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) 2.20.0 or higher
* [Python](https://www.python.org/downloads/) 3.9 or higher

### Windows

Install the Azure CLI using PowerShell according to the [official documentation](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-windows).

Then install the *absu* package with pip:

```bash
pip install absu
```

### Linux

Install the Azure CLI using PowerShell according to the [official documentation](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-linux).

Then install *absu* package with pip:

```bash
pip install absu
```

## How to use

Start by loggin into az:

```bash
az login
```

Then you can execute the tool with default parameters:

```bash
python -m absu
```

This will ask you for the name of the Azure Blob Storage name and for the local folder. If you have access to multiple subscriptions, then it will also ask you which subscription you want to use.

The resource group will be called "blob-rg".

---

Show help:

```bash
python -m absu -h
```

---

Provide a connection string:

```bash
python -m absu --connectionstring "DefaultEndpointsProtocol=https;AccountName=STORAGENAME;AccountKey=PASSWORD;EndpointSuffix=core.windows.net"
```

---

Provide a local folder (mywebsite) a storage account name (mystorage01) and a resource group (mybloggroup):

```bash
python -m absu --folder mywebsite --resourcegroup mybloggroup --storage mystorage01
```

---

Debugging:

```bash
python -m absu --verbose
```

---

General usage:

```
usage: __main__.py [-h] [-c CONNECTIONSTRING] [-s STORAGE] [-r RESOURCEGROUP] [-f FOLDER] [-v]       

Please provide at least one of the following: 1) a Azure Blob Storage name OR 2) a connection string.

optional arguments:
  -h, --help            show this help message and exit
  -c CONNECTIONSTRING, --connectionstring CONNECTIONSTRING
                        Azure Blob Storage connection string.
  -s STORAGE, --storage STORAGE
                        Azure Blob Storage resource name. Creates new one if not existing.
  -r RESOURCEGROUP, --resourcegroup RESOURCEGROUP
                        The Azure Blob Storage is in this resource group. Default: blogs-rg
  -f FOLDER, --folder FOLDER
                        Folder with static website data. Will be pushed to the storage.
  -v, --verbose         Verbose, use this flag for debugging.
  ```

## Build this project

Build locally:

```bash
pip install .
```

Build dist files:

```bash
python setup.py sdist
```

Upload to https://pypi.org:

```bash
twine upload dist/*
```