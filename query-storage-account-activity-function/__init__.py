import json
import os
from azure.appconfiguration import AzureAppConfigurationClient
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.data.tables import TableClient
from pathlib import Path

def main(request: dict) -> int:
    start = request['start']
    end   = request['end']
    
    table_conn_str = get_azure_table_connection_string()
    response = run_query(start, end, table_conn_str)

    return response

def run_query(start, end, table_conn_str) -> int:

    items = []
    client =  TableClient.from_connection_string(conn_str=table_conn_str, table_name="audit") 
    
    parameters = {
        "start": start,
        "end": end
    }
           
    query_filter = "PartitionKey ge @start and PartitionKey le @end and CertNumber ne ''"
    entities = client.query_entities(query_filter, parameters=parameters, select='identificationNumber')
    
    for entity in entities:
        items.append(entity['identificationNumber'])
        
    return len(set(items))

def get_azure_table_connection_string() -> str:
    
    defaultAzureCredential = DefaultAzureCredential()

    app_config_base_url = os.getenv('AppConfigEndpoint')
    app_config_client = AzureAppConfigurationClient(base_url=app_config_base_url, credential=defaultAzureCredential)

    keyvault_value = app_config_client.get_configuration_setting(key="storage-account-connection-string", label="async-http-api")
    url_parts = Path(json.loads(keyvault_value.value)["uri"]).parts
    vault_url = "//".join(url_parts[:2])
    kv_secret = url_parts[-1]
    kv_client = SecretClient(vault_url, defaultAzureCredential)
    secret_val = kv_client.get_secret(kv_secret).value

    return secret_val
