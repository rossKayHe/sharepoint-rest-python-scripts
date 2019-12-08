#! /bin/env python
import requests
import json
from requests_ntlm import HttpNtlmAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from spconfig import *

# from priv_config import *

# ~ Disable SLL warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# ~ Create credential to connect to SharePoint
auth = HttpNtlmAuth(sharepoint_user, sharepoint_password)

#
sp_rest_url = 'https://spteams/sites/ICC/_vti_bin/listdata.svc/'

# ~ Find SharePoint list item.  Returns metadata (.uri, .etag, .type) in json
# On success return code 200 with a body payload
def find_item(sharepoint_list, item_filter):
    sharepoint_url = sp_rest_url + sharepoint_list + '?$filter=' + item_filter
    headers = {
        'Accept': 'application/json; odata=verbose',
        'Content-Type': 'application/json; odata=verbose'
    }
    try:
        r = requests.get(sharepoint_url, headers=headers, auth=auth, verify=False)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        rtn = {
            "uri": "error",
            "etag": str(e.errno) + "  " + str(e.strerror)
        }
        return rtn

    data = json.loads(r.text)

    # validate only one record is returned
    if len(data['d']['results']) == 1:
        mdata = data['d']['results'][0]['__metadata']
        return mdata
    else:
        rtn = {
            "uri": "error",
            "etag": "query returned " + str(len(data['d']['results'])) + " item(s)"
        }
        return rtn


# UpSert funtion find record, if not found, create, else update
def upsert_item(sharepoint_list, item_filter, data):
    data_json = json.dumps(data)
    ups_data = find_item(sharepoint_list, item_filter)

    if str(ups_data['uri']) == "error":
        # create
        #print('error on find asserted')
        result = create_item(sharepoint_list, data_json)
        return result
    else:
        # update
        #print('No error on find asserted')
        result = update_item(sharepoint_list, item_filter, data_json)
        return result


# ~ Create SharePoint list item.  Pass the column data as data_json
# On success return code 201 with a body payload, same structure as parsed in the find_item
def create_item(sharepoint_list, data_json):
    sharepoint_url = sp_rest_url + sharepoint_list
    headers = {
        'Accept': 'application/json; odata=verbose',
        'Content-Type': 'application/json; odata=verbose'
    }
    try:
        r = requests.post(sharepoint_url, headers=headers, auth=auth, data=data_json, verify=False)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        return "error" + str(e.errno) + "  " + str(e.strerror)
    if r.status_code == 201:
        return "success"
    else:
        return "error unexpected return code: " + str(r.status_code)


# ~ Update SharePoint list item.  Pass the column changes as data_json
# On success return code 204, no body
def update_item(sharepoint_list, item_filter, data_json):
    # ~ Find item to update
    metadata = find_item(sharepoint_list, item_filter)
    headers = {
        'Accept': 'application/json; odata=verbose',
        'Content-Type': 'application/json; odata=verbose',
        'X-HTTP-Method': 'MERGE',
        'If-Match': metadata['etag']
    }

    try:
        r = requests.post(metadata['uri'], headers=headers, auth=auth, data=data_json, verify=False)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        return "error" + str(e.errno) + "  " + str(e.strerror)
    if r.status_code == 204:
        return "success"
    else:
        return "error unexpected return code: " + str(r.status_code)


# ~ Delete SharePoint list item.
# On success return code 204, no body
def delete_item(sharepoint_list, item_filter):
    # ~ Find item to delete
    metadata = find_item(sharepoint_list, item_filter)
    headers = {
        'Accept': 'application/json; odata=verbose',
        'Content-Type': 'application/json; odata=verbose',
        'X-HTTP-Method': 'DELETE',
        'If-Match': metadata['etag']
    }

    try:
        r = requests.post(metadata['uri'], headers=headers, auth=auth, verify=False)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        return "error" + str(e.errno) + "  " + str(e.strerror)
    if r.status_code == 204:
        return "success"
    else:
        return "error unexpected return code: " + str(r.status_code)
