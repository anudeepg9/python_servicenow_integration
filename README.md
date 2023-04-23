# Servicenow_Python_MySQL Integration for the Purpose of Automation
This Python script is designed to integrate ServiceNow and MySQL databases. It retrieves data from ServiceNow API, updates the data in MySQL database, and then updates the ServiceNow API with the results.

Getting Started:
To use this script, you will need to have the following:
-- A ServiceNow instance with API access
-- A MySQL database with proper credentials
-- Python 3.x installed

Installation:
Clone this repository to your local machine

Install the required Python packages using the following command:
pip install -r requirements.txt

-- Edit the snowInt class in the script to include your ServiceNow automation account credentials, endpoint URL, and proper headers.
-- Edit the my_sql_update method in the script to include your MySQL database credentials.

Run the script using the following command:
python service_now_mysql_integration.py

Usage:
The script retrieves ServiceNow tickets with the following criteria:
Active = True
State = 13   i.e, Requested State
Short Description contains the phrase "account status inactive"
-- Edit the geturl field in the script to change the above param query and personalise according to required filter

  Once a ticket is retrieved, the script will parse the incident data and extract relevant fields. It will then update the ticket's state to "Work in Progress" and execute a MySQL query to update the status of the user associated with the ticket. Finally, the script will update the ticket's state to "Closed Complete" and include the results of the MySQL query in the ticket's work notes.

If no tickets meet the specified criteria, the script will print a message indicating that there are no new tickets to process

Can also be included:
The service now request can be sent to approval of manager using a small flow in Service Now before it reaches to the automation queue to add extra security. For this we can chnage params query for filtering tickets with state = 15 i.e, Approved state.
