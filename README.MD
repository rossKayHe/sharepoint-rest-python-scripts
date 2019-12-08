**spClient_TibcoDeploymentTracker.py**
A client script for the TibcoDeploymentTracker List
It accepts 3 parameters:
1.	Archive_name
1.	Domain
1.	Git_Tag

It formats the input from the parameters and performs an upsert 

****************************************************
**spconfig.py**
This holds the values for *sharepoint_user*  and *sharepoint_password*

****************************************************
**spModl.py**
Module holding the CRUD SharePoint Operations
Contains the following functions

~ Find SharePoint list item.  Returns metadata (.uri, .etag, .type) in json
>    find_item(sharepoint_list, item_filter):

UpSert funtion find record, if not found, create, else update
>    upsert_item(sharepoint_list, item_filter, data):

~ Create SharePoint list item.  Pass the column data as data_json
On success return code 201 with a body payload, same structure as parsed in the find_item
>    create_item(sharepoint_list, data_json):

~ Update SharePoint list item.  Pass the column changes as data_json
On success return code 204, no body
>    update_item(sharepoint_list, item_filter, data_json):

~ Delete SharePoint list item.
On success return code 204, no body
>    delete_item(sharepoint_list, item_filter):

****************************************************
**spREST_Examples.txt**
Samples tested using the Chrome Rested client
