import logging
import azure.functions as func
from azure.cosmos import exceptions, CosmosClient, PartitionKey


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        endpoint = "https://pythondemo.documents.azure.com:443/"
        key = 'Qyxm4LRY5vEh41KzNz6HMFzqCbzLZDorySjzm1sZ26QSVduiEUuLOl96y5YA7jSemG7NLPIimdEQXiRWeSU4qA=='
        client = CosmosClient(endpoint, key)
        database_name = 'pythondemo'
        database = client.create_database_if_not_exists(id=database_name)
        container_name= 'container1'
        container = database.create_container_if_not_exists(id=container_name,partition_key=PartitionKey(path="/id"),offer_throughput=400)

        query = 'SELECT * FROM c WHERE c.name = "sneha"'
        items = list(container.query_items(query=query, enable_cross_partition_query=True))
        print("bla bla"+str(items))
        return func.HttpResponse("success", status_code=200)
        # return func.HttpResponse(
            #  "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            #  status_code=200
        # )
