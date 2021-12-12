import azure.durable_functions as df


def orchestrator_function(context: df.DurableOrchestrationContext):
    input = context.get_input()
    result = yield context.call_activity('query-storage-account-activity-function', {'start': input['start'], 'end': input['end']})
    return result

main = df.Orchestrator.create(orchestrator_function)