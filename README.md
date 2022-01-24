# vManagePolicyMgr
Basic tool for pushing entries into a policy.

Currently shows how to push a TLOC list using a CSV file.  This script can be adapted to other policy lists by modifying the CSV file and the URL's used for the GET and POST.  The CSV file will need to have the correct elements listed.  You can find these elements by pulling existing lists.  All lists can be retrieved using:
> https://{vmanage}/apidocs/#!/Configuration_-_Policy_List_Builder/getLists

Use the vManage Swagger interface to find the correct GET and POST URLs:

> https://{vmanage}/apidocs

# Basic Use Instructions
1. Clone repository
2. Install requirements

> pip install -p requirements

3. 
