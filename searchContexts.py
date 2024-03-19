#!/usr/bin/python3
# Get the list of users feature is enabled to

import http.client
import json
import csv

PROJECT_KEY = "omnibus-my-brand-mob"
API_KEY = "api-7d596d64-a5a9-423d-b071-542162f7e64b"
ENVIRONMENT_KEY = "production"
CONNECTION_URL = "app.launchdarkly.com"
FILTER = "user.appVersion equals 6.23.1,user.region equals NA,user.appBrand equals Buick"
SORT = "-ts"
LIMIT = "50"
featureFlagName = "msalEnhancementEnabled"
OUTPUT_FILE = "/Users/brad/Desktop/UserIdsMatchingCriteria-031624.csv"

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
    get_feature_flag_status_for_user("9dc0e39c-dd3f-4144-bd3d-6414c6ee0583")

if __name__ == "__main__":
  main()

