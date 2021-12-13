import azure.functions as func
import azure.durable_functions as df
import json
import dateutil.parser
from urllib.parse import urlparse

async def main(req: func.HttpRequest, starter: str) -> func.HttpResponse:

    response = { }
    headers = { "Content-Type": "application/json" }

    start_date = req.params.get('s')
    end_date = req.params.get('e')
    
    if start_date:
        try:
          start_date = dateutil.parser.parse(start_date, dayfirst=True)
        except:
          response['error'] = "Invalid start date format."
          return func.HttpResponse(json.dumps(response) ,headers=headers, status_code=400 )
    else:
        response['error'] = "Empty start date."
        return func.HttpResponse(json.dumps(response) ,headers=headers, status_code=400 )

    if end_date:
        try:
          end_date = dateutil.parser.parse(end_date, dayfirst=True)
        except:
          response['error'] = "Invalid end date format."
          return func.HttpResponse(json.dumps(response) ,headers=headers, status_code=400 )
    else:
        response['error'] = "Empty end date."
        return func.HttpResponse(json.dumps(response) ,headers=headers, status_code=400 )

    delta = end_date - start_date
    if delta.days < 1:
        response['error'] = "Invalid date range."
        return func.HttpResponse(json.dumps(response) ,headers=headers, status_code=400 )

    
    client = df.DurableOrchestrationClient(starter)

    parameters = {
        "start": start_date.strftime("%Y-%m-%d"),
        "end": end_date.strftime("%Y-%m-%d")
    }

    instance_id = await client.start_new('orchestrator-function', None, parameters)

    status_uri = build_api_url(urlparse(req.url).scheme, req.headers.get("host"), instance_id)
    response["statusUri"] = status_uri
    return func.HttpResponse(json.dumps(response), headers=headers, status_code=200 )

def build_api_url(scheme, host, instance_id):
    return f"{scheme}/{host}/api/status/{instance_id}"
