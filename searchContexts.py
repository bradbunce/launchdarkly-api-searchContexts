import os
import http.client
import json
import csv

def get_feature_flag_status_for_user(userId):
#Todo read the csv file and get flag status
    print("Evaluating Flag Status for userId: ", userId)
    evaluateUrlPath = "/api/v2/projects/" + os.environ['projectKey'] + "/environments/" + os.environ['environmentKey'] + "/flags/evaluate?filter=query%20equals%20" + os.environ['featureFlagKey']
    evaluatePayload = "{\"key\": \"" + userId + "\",\"kind\": \"user\"}"
    response = request_connection(evaluateUrlPath, evaluatePayload)
    print(response)
    
    
def request_connection(connectionUrlPath, payload):
    headers = {
      "Content-Type": "application/json",
      "Authorization": os.environ['apiKey']
    }
    conn = http.client.HTTPSConnection(os.environ['connectionUrl'])
    conn.request("POST", connectionUrlPath, payload, headers)
    response = conn.getresponse()
    data = response.read().decode("utf-8")
    if response.status == 200:
        return json.loads(data)
    else:
        print('Error getting the contexts: ', response.status, response.reason, data)
        return {}
        
def export_userIds_to_csv(items):
    file = open(os.environ['outputFile'], 'a')
    writer = csv.writer(file)
    for item in items:
        context = item["context"]
        userKey = context["key"]
        singleRow = [userKey]
        writer.writerow(singleRow)
    
def get_user_matching_contexts():
    connectionUrlPath = "/api/v2/projects/" + os.environ['projectKey'] + "/environments/" + os.environ['environmentKey'] + "/contexts/search"
    payload = "{\"filter\":\"" + os.environ['contextFilter'] + "\",\"sort\": \"" + os.environ['sort'] + "\",\"limit\": " + os.environ['limit'] + "}"
    contextResponse = request_connection(connectionUrlPath, payload)
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
            payload = "{\"filter\":\"" + os.environ['contextFilter'] + "\",\"sort\": \"" + os.environ['sort'] + "\",\"limit\": " + os.environ['limit'] + ",\"continuationToken\": \"" + continuationToken + "\"}"
            contextResponse = request_connection(connectionUrlPath, payload)
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
    get_feature_flag_status_for_user(os.environ['contextKey'])

if __name__ == "__main__":
  main()

