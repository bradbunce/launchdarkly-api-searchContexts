#!/usr/bin/python3
# Get the list of users feature is enabled to

import http.client
import json
import csv

PROJECT_KEY = "your-project-key"
API_KEY = "your-api-key"
ENVIRONMENT_KEY = "your-environment-key"
CONNECTION_URL = "app.launchdarkly.com"
FILTER = "your filter"
SORT = "ts or -ts"
LIMIT = "minimum value 20, maximum value 50"
featureFlagName = "your-flag-key"
OUTPUT_FILE = "local output file location"

def get_feature_flag_status_for_user(userId):
#Todo read the csv file and get flag status
    print("Evaluating Flag Status for userId: ", userId)
    evaluateUrlPath = "/api/v2/projects/" + PROJECT_KEY + "/environments/" + ENVIRONMENT_KEY + "/flags/evaluate?filter=query%20equals%20" + featureFlagName
    evaluatePayload = "{\"key\": \"" + userId + "\",\"kind\": \"user\"}"
    response = request_connection(evaluateUrlPath, evaluatePayload)
    print(response)
    
    
def request_connection(CONNECTION_URLPath, payload):
    headers = {
      "Content-Type": "application/json",
      "Authorization": API_KEY
    }
    conn = http.client.HTTPSConnection(CONNECTION_URL)
    conn.request("POST", CONNECTION_URLPath, payload, headers)
    response = conn.getresponse()
    data = response.read().decode("utf-8")
    if response.status == 200:
        return json.loads(data)
    else:
        print('Error getting the contexts: ', response.status, response.reason, data)
        return {}
        
def export_userIds_to_csv(items):
    file = open(OUTPUT_FILE, 'a')
    writer = csv.writer(file)
    for item in items:
        context = item["context"]
        userKey = context["key"]
        singleRow = [userKey]
        writer.writerow(singleRow)
    
def get_user_matching_contexts():
    CONNECTION_URLPath = "/api/v2/projects/" + PROJECT_KEY + "/environments/" + ENVIRONMENT_KEY + "/contexts/search"
    payload = "{\"filter\":\"" + FILTER + "\",\"sort\": \"" + SORT + "\",\"limit\": " + LIMIT + "}"
    contextResponse = request_connection(CONNECTION_URLPath, payload)
    if len(contextResponse) != 0:
        totalContextsCount = contextResponse["totalCount"]
        print("Total context count: ", totalContextsCount)
        contextsReturned = contextResponse["items"]
        contextsReturnedCount = len(contextsReturned)
        percentageContextsReturned = (contextsReturnedCount/totalContextsCount)*100
        print("Total contexts returned: ", contextsReturnedCount, "out of",totalContextsCount, "- Percent of total contexts returned: ","%.2f%%" % percentageContextsReturned)

        while len(contextsReturned) != 0:
            export_userIds_to_csv(contextsReturned)
            continuationToken = contextResponse["continuationToken"]
            payload = "{\"filter\":\"" + FILTER + "\",\"sort\": \"" + SORT + "\",\"limit\": " + LIMIT + ",\"continuationToken\": \"" + continuationToken + "\"}"
            contextResponse = request_connection(CONNECTION_URLPath, payload)
            if len(contextResponse) != 0:
                contextsReturned = contextResponse["items"]
                additionalContextsReturnedCount = len(contextsReturned)
                print("Additional contexts returned during refresh: ", additionalContextsReturnedCount)
                sumContextsReturnedCount = contextsReturnedCount + additionalContextsReturnedCount
                percentageContextsReturned = (sumContextsReturnedCount/totalContextsCount)*100
                print("Total contexts returned: ", sumContextsReturnedCount, "out of",totalContextsCount, "- Percent of total contexts returned: ","%.2f%%" % percentageContextsReturned)
                contextsReturnedCount = sumContextsReturnedCount
            else:
                break
        print('Retreived all userIds')
            
    else:
        print('Cannot get userIds, EXITING!!!!')


def main():
    response = get_user_matching_contexts()
    get_feature_flag_status_for_user("context-key")

if __name__ == "__main__":
  main()

