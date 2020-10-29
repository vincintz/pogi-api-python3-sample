import sys
# Import the requests library (the rest of the examples assumes is already imported)
import requests

pogi_url = "https://www.-.com:7000" # Insert your Pogi server URL here
user_id = ""  # Insert your Pogi user ID here
user_pwd = "" # Insert your Pogi password here

if not user_id or not user_pwd:
    print("You'll need a valid URL, user id and password to connect to PogiAPI")
    sys.exit()


print("GET the version info")
version_rs = requests.get(pogi_url, params={ "op": "version" })

# Check the return status, and print the response text
if (version_rs.status_code == 200):
    print(version_rs.text)
else:
    print('Something went wrong')

print("Authenticate via username and password (returns token)")
# POST auth
token_rs = requests.post(pogi_url, params={ "op": "token-get", "userId": user_id, "password": user_pwd })

# Check the return status, and print the response text
if (token_rs.status_code == 200):
    print(token_rs.text)
else:
    print('Something went wrong')


print("Store Token from response")
token_data = token_rs.json()
print(token_data, token_data["token"])
if "token" in token_data:
    token = token_data["token"]
    print("Token: " + token)
elif "error" in token_data:
    print("Error: " + token_data["error"])
else:
    print("Unknown error encountered")


print("Get inventory history list")
inventory_params = {
    "op": "history",
    "token": token,
    "fromDate": "",
    "fromTime": "",
    "toDate": "",
    "toTime": "",
    "marker": "",
    "event": "present",
    "zone": "",
    "limit": 15,
    "offSet": 0,
    "currentLocation": "on",
    "namedOnly": "",
    "tagAssetSearchType": "tag",
    "tagAndAssetSearchType": "tag",
    "tagAndAsset": "",
    "orderColumn": "update_date",
    "orderDirection": "DESC"
}
inventory_rs = requests.post(pogi_url, params=inventory_params)
# Check the return status, and print the response text
if (inventory_rs.status_code == 200):
    print(inventory_rs.text)
    print(inventory_rs.json()['count'])
    print(len(inventory_rs.json()['data']))
    print("Loop through the items")
    for item in inventory_rs.json()['data']:
        print("Tag: {}; Name: {}".format(item['tag_id'], item['name']))
else:
    print('Something went wrong')

print("Get item by tag")
# POST request
payload = {
  "op": "id-get",
  "token": token,
  "tag": "000000000000000000000000"
}
id_get_rs = requests.post(pogi_url, params=payload)

# Check the return status, and print the response text
if (id_get_rs.status_code == 200):
    print(id_get_rs.json())
    print('id-get returned {} result/s'.format(len(id_get_rs.json())))
    if len(id_get_rs.json()) > 0:
        data = id_get_rs.json()[0]
        print('Tag: {}; Location: {}'.format(data['tag_id'], data['zone']))
else:
    print('Something went wrong')

print("Delete Item")
print("Make sure to clear undelete info for the tag")
payload = {
  "op": "id-undelete",
  "token": token,
  "tagId": "000000000000000000000000"
}
id_undelete_rs = requests.post(pogi_url, params=payload)
# Check the return status, and print the response text
if (id_undelete_rs.status_code == 200):
    print(id_undelete_rs.json())
else:
    print('Something went wrong')

print("Then call delete")
# POST request
payload = {
  "op": "id-delete",
  "token": token,
  "tagId": "000000000000000000000000"
}
id_delete_rs = requests.post(pogi_url, params=payload)
# Check the return status, and print the response text
if (id_delete_rs.status_code == 200):
    print(id_delete_rs.json())
else:
    print('Something went wrong')

print("Create Item")
# POST request
payload = {
  "op": "id-add",
  "token": token,
  "tagId": "000000000000000000000000",
  "external_id": "Asset ID",
  "name": "QuickTag Demo",
  "zone": "Laboratory"
}
id_add_rs = requests.post(pogi_url, params=payload)

# Check the return status, and print the response text
if (id_add_rs.status_code == 200):
    print('Item created')
else:
    print('Something went wrong')


print("Update Item")
# POST request
payload = {
  "op": "id-update",
  "token": token,
  "tagId": "000000000000000000000000",
  "external_id": "Asset ID Updated",
  "name": "QuickTag Demo Updated",
  "zone": "Laboratory"
}
id_update_rs = requests.post(pogi_url, params=payload)

# Check the return status, and print the response text
if (id_update_rs.status_code == 200):
    print('Item updated')
else:
    print('Something went wrong')
