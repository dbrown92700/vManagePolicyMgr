# vManagePolicyMgr

Basic tool for pushing policy elements into a policy.

### Current State:

Script currently shows how to push a TLOC list or Data Prefix list using a CSV file.

### Options for expanding functionality:

This script can be adapted to other policy lists by modifying the CSV file and the URL's used for the GET and POST.  The CSV file will need to have the correct elements listed.  You can find these elements by pulling existing lists.  All lists can be retrieved using:
> https://{vmanage}/apidocs/#!/Configuration_-_Policy_List_Builder/getLists

Use the vManage Swagger interface to find the correct GET and POST URLs:

> https://{vmanage}/apidocs

# Basic Use Instructions
1. Clone repository

> git clone https://github.com/dbrown92700/vManagePolicyMgr

2. Recommend using a virtual environment

> cd vManagePolicyMgr
>
> python3 -m venv venv
> 
> source venv/bin/activate

3. Install requirements

> pip install -p requirements

4. Edit list.csv file

5. Run main.py

> python3 main.py
