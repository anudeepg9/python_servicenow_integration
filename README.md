# Python_Servicenow_MySQL Integration for the Purpose of Automation
This Project has a python script which automates the process of changing an account status to Active in mySQL db when a request is raised in ServiceNow.

The Python Script: # connects with servicenow instance via api and gets the new requests by filtering the available requests using short description field and the approval status. # gets the UserID field from my Service Now developer Portal when a request is raised in NEEDIT application (present in my devtraining-needit branch) # then connects to the mySQLdb which is given as local host currently and unlocks the account status by running a update query. # depending on the query status updates the servicenow ticket with the required information and closes the ticket if work is done else changes to appropriate state according to the query result.

Handled exceptions using try-catch.

Initially the service now request goes to approval of the manager and it then reached to the automation queue only if approved. Designed a small flow in Service Now for the same.
