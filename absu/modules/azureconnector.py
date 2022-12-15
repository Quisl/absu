"""Provides a class that handles general communication with Azure"""
import logging
import os
import json
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.subscription import SubscriptionClient
from azure.identity import AzureCliCredential
from azure.core.exceptions import ClientAuthenticationError
from azure.mgmt.resource.resources.models import DeploymentMode, Deployment
from azure.core.exceptions import HttpResponseError
from .templates.storage import TEMPLATE


class AzureConnector:
    """This class handles Azure connections and can create/update resources"""

    def __init__(self):
        self.credential = AzureCliCredential()
        self.subscriptionId = self.get_subscription()
        self.location = "westeurope"
        self.resourceClient = ResourceManagementClient(
            self.credential, self.subscriptionId
        )

    def __select_subscription(self, subs):
        print("Found multiple subscriptions...")
        for idx, sub in enumerate(subs):
            print(f"{str(idx+1)}: {str(sub)}")
        subscription_option = int(input("Select number: ")) - 1
        print(type(subscription_option))
        return subs[subscription_option][1]

    def __run_az_login(self):
        logging.info("Not logged in, running az login")
        output = os.popen("az login").read()
        logging.info("Az login results... %s", output)

    def get_subscription(self):
        """returns a subscription id. executes az login if not logged in"""
        try:
            sub_client = SubscriptionClient(self.credential)
        except ClientAuthenticationError:
            self.__run_az_login()
            sub_client = SubscriptionClient(self.credential)
        subscription = sub_client.subscriptions.list()
        subs = [
            [sub.display_name, sub.subscription_id]
            for sub in subscription
        ]
        if len(subs) == 1:
            result = subs[0][1]
        else:
            result = self.__select_subscription(subs)
        return result

    def get_connection_string(self, storage, resourcegroup):
        """gets a connection string from"""
        return json.loads(
            os.popen(
                f"az storage account show-connection-string --name {storage} "
                f"--resource-group {resourcegroup} "
                f"--subscription {self.subscriptionId}"
            ).read()
        )["connectionString"]

    def get_storage_account_web_endpoint(self, storage, resourcegroup):
        """returns the address of the web endpoint"""
        return self.resourceClient.resources.get(
            resource_group_name=resourcegroup,
            resource_provider_namespace="Microsoft.Storage",
            api_version="2022-05-01",
            resource_name=storage,
            parent_resource_path="",
            resource_type="storageAccounts",
        ).__dict__["properties"]["primaryEndpoints"]["web"]

    def create_resource_group(self, resourcegroup):
        """creates a resource group"""
        rg_result = self.resourceClient.resource_groups.create_or_update(
            resourcegroup, {"location": self.location}
        )

        logging.debug(rg_result)

    def create_storage_account(self, resourcegroup, storage):
        """creates a storage (as defined in templates/storage.py)"""
        parameters = {
            "storageAccounts_blogdatastore_name": storage,
        }
        parameters = {k: {"value": v} for k, v in parameters.items()}
        deployment_properties = {
            "mode": DeploymentMode.incremental,
            "template": TEMPLATE,
            "parameters": parameters,
        }
        try:
            deployment_async_operation = self.resourceClient.deployments.begin_create_or_update(
                resource_group_name=resourcegroup,
                deployment_name="azure-sample",
                parameters=Deployment(
                    tags=None,
                    # location="westeurope",
                    properties=deployment_properties,
                ),
            )
            deployment_async_operation.wait()
            result = True
        except HttpResponseError:
            result = False
        return result
