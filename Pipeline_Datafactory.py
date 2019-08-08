import os
import traceback
from azure.common.credentials import ServicePrincipalCredentials
from msrestazure.azure_exceptions import CloudError
from msrestazure.azure_configuration import AzureConfiguration
from msrest.service_client import ServiceClient
from msrest.polling import LROPoller
from msrestazure.polling.arm_polling import ARMPolling
from msrest.pipeline import ClientRawResponse
import uuid

from dotenv import load_dotenv


project_folder = os.path.expanduser("/home/admin1/Desktop/Gayatri/API_All/venv") # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))


SUBSCRIPTION_ID = os.environ.get('AZURE_SUBSCRIPTION_ID')
RESOURCE_GROUP = "APIResourceGroup"
FACTORY_NAME = "gayatritestDataFactory"
PIPELINE_NAME = "PythonScriptPipelineTesting"

BODY = {
  "properties": {
    "activities": [
      {
        "type": "ForEach",
        "typeProperties": {
          "isSequential": True,
          "items": {
            "value": "@pipeline().parameters.OutputBlobNameList",
            "type": "Expression"
          },
          "activities": [
            {
              "type": "Copy",
              "typeProperties": {
                "source": {
                  "type": "BlobSource"
                },
                "sink": {
                  "type": "BlobSink"
                },
                "dataIntegrationUnits": "32"
              },
              "inputs": [
                {
                  "referenceName": "TestDataset",
                  "parameters": {
                    "MyFolderPath": "examplecontainer",
                    "MyFileName": "examplecontainer.csv"
                  },
                  "type": "DatasetReference"
                }
              ],
              "outputs": [
                {
                  "referenceName": "TestDataset",
                  "parameters": {
                    "MyFolderPath": "examplecontainer",
                    "MyFileName": {
                      "value": "@item()",
                      "type": "Expression"
                    }
                  },
                  "type": "DatasetReference"
                }
              ],
              "name": "ExampleCopyActivity"
            }
          ]
        },
        "name": "ExampleForeachActivity"
      }
    ],
    "parameters": {
      "OutputBlobNameList": {
        "type": "Array"
      }
    },
    "variables": {
      "TestVariableArray": {
        "type": "Array"
      }
    }
  }
}

API_VERSION = '2018-06-01'

def get_credentials():
    credentials = ServicePrincipalCredentials(
        client_id=os.environ.get('AZURE_CLIENT_ID'),
        secret=os.environ.get('AZURE_CLIENT_SECRET'),
        tenant=os.environ.get('AZURE_TENANT_ID')
    )
    return credentials


def run_example():
    credentials = get_credentials()

    config = AzureConfiguration('https://management.azure.com')
    service_client = ServiceClient(credentials, config)

    query_parameters = {}
    query_parameters['api-version'] = API_VERSION

    header_parameters = {}
    header_parameters['Content-Type'] = 'application/json; charset=utf-8'

    operation_config = {}
    request = service_client.put("/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.DataFactory/factories/" + FACTORY_NAME + "/pipelines/" + PIPELINE_NAME, query_parameters)
    response = service_client.send(request, header_parameters, BODY, **operation_config)
    print(response.text)


if __name__ == "__main__":
    run_example()