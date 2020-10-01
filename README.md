# PogiAPI - Python3

Connecting to PogiAPI via Python3 interpreter using Python's [request library](https://requests.readthedocs.io/en/master/)

Pogi API enpoints are accessible either via GET or POST requests. The `op` parameter determines the operation. Sample operations:

| op         | Description |
| :---:      |:---         |
|get-version | Returns the current API version |
|get-token   | Returns the token used for authentication |
|history     | Search for items |
|id-get      | Get item by tag-id |
|id-add      | Create new item  |
|id-update   | Edit existing item by tag-id |
|id-delete   | Deiete an item by tag-id|



## Prerequisites
1. Python3 and pip3 installed
2. Python request library [installed](https://requests.readthedocs.io/en/master/user/install/#install)

To start the interpreter, run python3 from the command line
```
% python3

Python 3.8.5 (default, Jul 21 2020, 10:48:26)
[Clang 11.0.3 (clang-1103.0.32.62)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
```

## Get API version info

* **op** = get-version

* **Get version** (Note: replace `snoke.simplyrfid.com` with the actual API URL)
  ```
  # Import the requests library (the rest of the examples assumes is already imported)
  import requests

  # GET the version info
  version_rs = requests.get(pogi_url, params={ "op": "get-version" })

  # Check the return status, and print the response text
  if (version_rs.status_code == 200):
      print(version_rs.text)
  else:
      print('Something went wrong')
  ```

* **Output**
  ```
  '{"message": "3.00.04", "version": "3.00.04", "versionWave": "3.00.03", "response": "OK"}'
  ```

## Authenticate via username and password (returns token)

* **Prereq** You'll need a valid URL, user id and password to connect to PogiAPI
  ```
  pogi_url = 'https://www.-.com:7000' # Insert your Pogi server URL here
  user_id = ""  # Insert your Pogi user ID here
  user_pwd = "" # Insert your Pogi password here
  ```  
* **op** = token-get
* **Authenticate** (Note: Replace the userId and password)
  ```
  # POST auth
  token_rs = requests.post(pogi_url, data={ "op": "token-get", "userId": user_id, "password": user_pwd })

  # Check the return status, and print the response text
  if (token_rs.status_code == 200):
      print(token_rs.text)
  else:
      print('Something went wrong')
  ```
* **Output**
  ```
  {"org": "simplyrfid", "token": "96ab92c8fbe311eabcb906725332961a"}
  ```
  **or**
  ```
  {"response": "error", "error": "Invalid Login"}
  ```
* **Store Token from response**
  ```
  token_data = token_rs.json()
  if "token" in token_data:
      token = token_data["token"]
      print("Token: " + token)
  elif "error" in token_data:
      print("Error: " + token_data["error"])
  else:
      print("Unknown error encountered")
  ```
* **Output**
  ```
  Token: 96ab92c8fbe311eabcb906725332961a
  ```

**Notes**
* The rest of the examples assumes that token is stored in a variable named `token`
* For web-applications, it is not necessary to store the token, this is passed by the browser to the server via cookies
* The example below shows how we can check the cookie using Python
  ```
  print(token_rs.headers['Set-Cookie'])
  ```
* **Output**
  ```
  Pogi=96ab92c8fbe311eabcb906725332961a;Secure;SameSite=None;
  ```

## Get inventory history list
* **op** = history
* **Set request paramters** (Note: requires the `token` from the previous step)
  ```
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
  ```
* **Get inventory history list**
  ```
  inventory_rs = requests.post(pogi_url, data=inventory_params)
  # Check the return status, and print the response text
  if (inventory_rs.status_code == 200):
      print(inventory_rs.text)
  else:
      print('Something went wrong')
  ```
* **Sample response checks**
  * Print the total number of items
    ```
    print(inventory_rs.json()['count'])
    ```
  * Output
    ```
    {'total': 1465}
    ```
  * Print the number of items returned (comtrolled by the `limit` parameter)
    ```
    print(len(inventory_rs.json()['data']))
    ```
  * Output
    ```
    15
    ```
  * Loop through the items
    ```
    for item in inventory_rs.json()['data']:
        print("Tag: {}; Name: {}".format(item['tag_id'], item['name']))
    ```


## Get item by tag
* **op** = id-get
* **Get item**
  ```
  # POST request
  payload = {
    "op": "id-get",
    "token": token,
    "tag": "000000000000000000000000"
  }
  id_get_rs = requests.post(pogi_url, data=payload)

  # Check the return status, and print the response text
  if (id_get_rs.status_code == 200):
      print(id_get_rs.json())
  else:
      print('Something went wrong')
  ```
* **Check result**
  ```
  print('id-get returned {} result/s'.format(len(id_get_rs.json())))
  ```
* **Print fields**
  ```
  if len(id_get_rs.json()) > 0:
      data = id_get_rs.json()[0]
      print('Tag: {}; Location: {}'.format(data['tag_id'], data['zone']))
  ```

## Delete Item

This is a two step process.
1. Make sure to clear undelete info for the tag (op=id-undelete)
2. Then call delete (op=id-delete)

### Make sure to clear undelete info for the tag
* **op** = id-undelete
* Clear undelete info
  ```
  # POST request
  payload = {
    "op": "id-undelete",
    "token": token,
    "tagId": "000000000000000000000000"
  }
  id_undelete_rs = requests.post(pogi_url, data=payload)
  # Check the return status, and print the response text
  if (id_undelete_rs.status_code == 200):
      print(id_undelete_rs.json())
  else:
      print('Something went wrong')
  ```

### Then call delete
* **op** = id-delete
* Call delete
  ```
  # POST request
  payload = {
    "op": "id-delete",
    "token": token,
    "tagId": "000000000000000000000000"
  }
  id_delete_rs = requests.post(pogi_url, data=payload)
  # Check the return status, and print the response text
  if (id_delete_rs.status_code == 200):
      print(id_delete_rs.json())
  else:
      print('Something went wrong')
  ```


## Create Item
* **op** = id-add
* **Create item**
  ```
  # POST request
  payload = {
    "op": "id-add",
    "token": token,
    "tagId": "000000000000000000000000",
    "external_id": "Asset ID",
    "name": "QuickTag Demo",
    "zone": "Laboratory"
  }
  id_add_rs = requests.post(pogi_url, data=payload)
  ```
* **Check the status**
  ```
  # Check the return status, and print the response text
  if (id_add_rs.status_code == 200):
      print(id_add_rs.json())
  else:
      print('Something went wrong')
  ```


## Update Item
* **op** = id-add
* **Update item**
  ```
  # POST request
  payload = {
    "op": "id-update",
    "token": token,
    "tagId": "000000000000000000000000",
    "external_id": "Asset ID Updated",
    "name": "QuickTag Demo Updated",
    "zone": "Laboratory"
  }
  id_update_rs = requests.post(pogi_url, data=payload)
  ```
* **Check the status**
  ```
  # Check the return status, and print the response text
  if (id_update_rs.status_code == 200):
      print(id_update_rs.json())
  else:
      print('Something went wrong')
  ```
