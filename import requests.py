import requests
import http.client
import json
import csv

project_key = "omnibus-my-brand-mob"
environment_key = "production"
connectionUrl = "app.launchdarkly.com"
url = "https://app.launchdarkly.com/api/v2/projects/" + project_key + "/environments/" + environment_key + "/contexts/search"
featureFlagName = "msalEnhancementEnabled"
outputFileName = "/Users/brad/Desktop/UserIdsMatchingCriteria-031624.csv"

payload = {
  "filter": "user.appVersion equals 6.23.1,user.region equals NA,user.appBrand equals Buick",
  "sort": "-ts",
  "limit": 50
}

headers = {
  "Content-Type": "application/json",
  "Authorization": "api-7d596d64-a5a9-423d-b071-542162f7e64b"
}

response = requests.post(url, json=payload, headers=headers)
    
data = response.json()
print(data)

def request_connection(connectionUrlPath, payload):
    print("Refreshing..............")
    conn = http.client.HTTPSConnection(connectionUrl)
    conn.request("POST", url, payload, headers)
    response = conn.getresponse()
    data = response.read().decode("utf-8");
    if response.status == 200:
        return json.loads(data)
    else:
        print('Error getting the contexts: ', response.status, response.reason, data)
        return {}

def get_user_matching_contexts():
    contextResponse = request_connection(url)
    if len(contextResponse) != 0:
        print("totalCount: ", contextResponse["totalCount"])
        items = contextResponse["items"]
        print("item length: ", len(items))
        
        while len(items) != 0:
            export_userIds_to_csv(items)
            links = contextResponse["_links"]
            next = links["next"];
            continuationUrlPath = next["href"]
            contextResponse = request_connection(continuationUrlPath, payload)
            if len(contextResponse) != 0:
                items = contextResponse["items"]
                print("item length during refresh: ", len(items))
            else:
                break
        print('Retreived all userIds')
            
    else:
        print('Cannot get userIds, EXITING!!!!')

def export_userIds_to_csv(items):
    data_file = open(outputFileName, 'a')
    csv_writer = csv.writer(data_file)
    for item in items:
        context = item["context"]
        userKey = context["key"]
        singleRow = [userKey]
        csv_writer.writerow(singleRow)

def main():
    get_user_matching_contexts()

if __name__ == "__main__":
  main()
