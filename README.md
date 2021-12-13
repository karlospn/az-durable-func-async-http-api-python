# Building an Async HTTP Api with Azure Durable functions and Python

The **async HTTP API** pattern addresses the problem of coordinating the state of long-running operations with external clients.   

A common way to implement this pattern is by having an HTTP endpoint trigger the long-running action. Then, redirect the client to a status endpoint that the client polls to learn when the operation is finished.

Azure Durable Functions provides built-in support for this pattern.

![async-pattern](https://docs.microsoft.com/en-us/azure/azure-functions/durable/media/durable-functions-concepts/async-http-api.png)


# Repository content

It contains an example about how to implement an async Http Api using Azure Durable functions and Python.
  
Here's a diagram that shows the dependencies between the different Azure Functions that you can find in this repository.

![diagram](https://raw.githubusercontent.com/karlospn/az-durable-func-async-http-api-python/main/docs/app-diagram.png)

- ``client-function``: submits the job that needs to be executed.
- ``get-status-function``: it is used to retrieve the status and the result of the submitted job.
- ``orchestrator-function``: Unwraps the parameters from the submitted job and calls the activity function.
- ``query-storage-account-activity-function``: Runs a custom query in an Azure Storage Table.   
The Azure Storage Table connection string is stored in an Azure App Configuration.