#! /bin/env python
import spModl
import json
import sys

sharepoint_list = 'TibcoDeploymentTracker'

#### Create list item data from arguments ####
data = {"Archive_name": str(sys.argv[1]),
        str(sys.argv[2]).capitalize(): str(sys.argv[3])
        }

item_filter= 'Archive_name eq \'' + str(sys.argv[1]) + '\''
# print(data)
# print(item_filter)

# create test
result = spModl.upsert_item(sharepoint_list, item_filter, data)
print(result)
