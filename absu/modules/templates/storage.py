"""template for azure"""
TEMPLATE = {
    "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
    "contentVersion": "1.0.0.0",
    "parameters": {
        "storageAccounts_blogdatastore_name": {
            "defaultValue": "blogdatastore",
            "type": "String",
        }
    },
    "variables": {},
    "resources": [
        {
            "type": "Microsoft.Storage/storageAccounts",
            "apiVersion": "2022-05-01",
            "name": "[parameters('storageAccounts_blogdatastore_name')]",
            "location": "westeurope",
            "sku": {"name": "Standard_LRS", "tier": "Standard"},
            "kind": "StorageV2",
            "properties": {
                "dnsEndpointType": "Standard",
                "defaultToOAuthAuthentication": False,
                "publicNetworkAccess": "Enabled",
                "allowCrossTenantReplication": True,
                "routingPreference": {
                    "routingChoice": "InternetRouting",
                    "publishMicrosoftEndpoints": False,
                    "publishInternetEndpoints": False,
                },
                "minimumTlsVersion": "TLS1_0",
                "allowBlobPublicAccess": True,
                "allowSharedKeyAccess": True,
                "networkAcls": {
                    "bypass": "AzureServices",
                    "virtualNetworkRules": [],
                    "ipRules": [],
                    "defaultAction": "Allow",
                },
                "supportsHttpsTrafficOnly": True,
                "encryption": {
                    "requireInfrastructureEncryption": False,
                    "services": {
                        "file": {"keyType": "Account", "enabled": True},
                        "blob": {"keyType": "Account", "enabled": True},
                    },
                    "keySource": "Microsoft.Storage",
                },
                "accessTier": "Hot",
            },
        }
    ],
}
