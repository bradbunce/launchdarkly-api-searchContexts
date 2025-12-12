import os
import http.client
import json
import csv
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def request_connection(connectionUrlPath, payload):
    headers = {
      "Content-Type": "application/json",
      "Authorization": os.environ['apiKey']
    }
    conn = http.client.HTTPSConnection(os.environ["connectionUrl"])
    conn.request("POST", connectionUrlPath, payload, headers)
    response = conn.getresponse()
    data = response.read().decode("utf-8")
    if response.status == 200:
        return json.loads(data)
    else:
        print("*** Error getting the contexts: ", response.status, response.reason, data)
        return {}
        
def export_contexts_to_csv(contexts):
    file = open(os.environ["outputFile"], "a")
    writer = csv.writer(file)
    headerRow = "Context Kind","Context Key"
    writer.writerow(headerRow)
    for item in contexts:
        context = item["context"]
        contextKind = context["kind"]
        contextKey = context["key"]
        singleRow = [contextKind,contextKey]
        writer.writerow(singleRow)

def export_contexts(contexts):
    contextKeyArray = []
    for item in contexts:
        context = item["context"]
        contextKey = context["key"]
        if contextKey != "":
            contextKeyArray.append(contextKey)
        else:
            break
    contextKeys = list(set(contextKeyArray))
    return(contextKeys)
            
def get_contexts():
    connectionUrlPath = "/api/v2/projects/" + os.environ['projectKey'] + "/environments/" + os.environ['environmentKey'] + "/contexts/search"
    payload = "{\"filter\":\"" + os.environ['contextFilter'] + "\",\"sort\": \"" + os.environ['sort'] + "\",\"limit\": " + os.environ['limit'] + "}"
    contextResponse = request_connection(connectionUrlPath, payload)
    if len(contextResponse) != 0:
        totalContextsCount = contextResponse["totalCount"]
        print("*** Total context count: ", totalContextsCount)
        contextsReturned = contextResponse["items"]
        contextsReturnedCount = len(contextsReturned)
        percentageContextsReturned = (contextsReturnedCount/totalContextsCount)*100
        print("*** Total contexts returned: ", contextsReturnedCount, "out of",totalContextsCount, "- Percent of total contexts returned: ","%.2f%%" % percentageContextsReturned)
        contexts = contextsReturned
        while (contextsReturnedCount) < (totalContextsCount):
            continuationToken = contextResponse["continuationToken"]
            payload = "{\"filter\":\"" + os.environ['contextFilter'] + "\",\"sort\": \"" + os.environ['sort'] + "\",\"limit\": " + os.environ['limit'] + ",\"continuationToken\": \"" + continuationToken + "\"}"
            contextResponse = request_connection(connectionUrlPath, payload)
            if len(contextResponse) != 0:
                contextsReturned = contextResponse["items"]
                additionalContextsReturnedCount = len(contextsReturned)
                print("*** Additional contexts returned during refresh: ", additionalContextsReturnedCount)
                sumContextsReturnedCount = contextsReturnedCount + additionalContextsReturnedCount
                percentageContextsReturned = (sumContextsReturnedCount/totalContextsCount)*100
                print("*** Total contexts returned: ", sumContextsReturnedCount, "out of",totalContextsCount, "- Percent of total contexts returned: ","%.2f%%" % percentageContextsReturned)
                contextsReturnedCount = sumContextsReturnedCount
                contexts.extend(contextsReturned)
            else:
                break
            print("*** Retreived all contexts! ***")
        return contexts
    else:
        print("*** Cannot get contexts, exiting! ***")
        return []

def get_feature_flag_variations_for_contexts(contextKeys):
    for contextKey in contextKeys:
        print("Evaluating flag values for context: ", contextKey)
        evaluateUrlPath = "/api/v2/projects/" + os.environ['projectKey'] + "/environments/" + os.environ['environmentKey'] + "/flags/evaluate"
        evaluatePayload = "{\"key\": \"" + contextKey + "\",\"kind\": \"user\"}"
        flagEvaluation = request_connection(evaluateUrlPath, evaluatePayload)
        flagValues = flagEvaluation["items"]
        for flag in flagValues:
            flagName = flag["name"]
            flagKey = flag["key"]
            flagValue = flag["_value"]
            print(flagName,flagKey,flagValue)
        time.sleep(2)

def main():
    response = get_contexts()
    if response:
        # export_contexts_to_csv(response)
        contextKeys = export_contexts(response)
        get_feature_flag_variations_for_contexts(contextKeys)
    else:
        print("*** No contexts retrieved. Please check your API key and configuration. ***")

if __name__ == "__main__":
  main()

