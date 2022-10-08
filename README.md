# *absu*: Azure Blob Storage Updater

## What is it?

*absu* is a tool that helps you syncing a local folder to the $web container of an Azure Blob Storage. This is useful if you want to host a website that was generated with a static website generator like [hugo](https://gohugo.io/), [mkdocs](https://www.mkdocs.org/), [Jekyll](https://jekyllrb.com/), [next.js](https://nextjs.org/) and so on on Azure Blob Storage...

*absu* does the following things:

* create a resource group in Azure (if not existing)
* create a Storage Account within that resource group (if not existing)
* create a $web container within that storage (if not existing)
* delete all files in that container
* upload all data from a local folder into that container

You can skip the first two steps by providing a connection string for an existing Azure Blob Storage.

## How to install

You will need these tools installed:
* [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) 2.20.0 or higher
* [Python](https://www.python.org/downloads/) 3.9 or higher

Use the following commands to make sure your installations works.

Python: 

```bash
python --version
```

Pip:

```bash
pip --version
```

Az:

```bash
az --version
```

---

Then install the *absu* package with pip:

```bash
pip install absu
```

## How to use

Show help:

```bash
python -m absu -h
```

```txt
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

---

Execute the tool with default parameters:

```bash
python -m absu
```

*absu* will ask you for the Azure Blob Storage name and for the local folder in the command line. If you have access to multiple subscriptions, then it will also ask you which subscription you want to use.

The resource group will be called "blob-rg" per default. It can be changed with the --resourcegroup parameter.

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

## Build this project

Build locally:

```bash
pip install .
```

Build dist files:

```bash
python setup.py sdist
```

Upload to https://test.pypi.org:

```bash
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

Upload to https://pypi.org:

```bash
twine upload dist/*
```