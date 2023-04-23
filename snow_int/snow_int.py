import requests
import mysql.connector

def main():
       
       #Getting data from servicenow and storing it in data var
    try: 
       data = snowInt.get_snow_ticket()

       # Parse incident data and extract relevant fields
       global userid
       userid = data.get('u_requested_for')
       number = data.get('number')
       desc = data.get('short_description')
       ass_group = data.get('assignment_group')
       state = data.get('state')
       sysid = data.get('sys_id')
       print(number, desc, ass_group, state, userid, sysid)

       #Updating ticket as Work in Progress
       snowInt.patch_snow_ticket(sysid, 'UpdateTicket', 0, data)

       #Querying the DB and storing the output
       rows_affected = snowInt.my_sql_update(userid)

       #Updating ticket as Closed Complete
       snowInt.patch_snow_ticket(sysid, '', rows_affected, data) 
    except:
        print("Currently, there are no new tickets to process")



class snowInt:
       
    # Setting up ServiceNow Automation Account Credentials
    global user, password, endpoint, headers
    user = 'python_auto'
    password = ' YOUR PASSWORD '
    endpoint = 'https://dev141170.service-now.com/api/now/table/x_58872_needit_needit'
    # Set proper headers
    headers = {"Content-Type":"application/json","Accept":"application/json"}

    def get_snow_ticket():
        # Set up ServiceNow GET API endpoint
        geturl = endpoint + '?' +'sysparm_query=active%3Dtrue%5Estate%3D13%5Eshort_descriptionLIKEaccount%20status%20inactive&sysparm_display_value=true&sysparm_exclude_reference_link=true&sysparm_limit=10'
        ##sysparm_fields=number%2Cu_requested_for%2Cstate%2Cshort_description&
 
        # Do the HTTP request
        response = requests.get(geturl, auth=(user, password), headers=headers)

        # Connect to ServiceNow API and retrieve incident record
        if response.status_code != 200:
            print('Error connecting to ServiceNow API: {}'.format(response.text))
            exit()
        data = response.json().get('result')[0]
        return data

    def patch_snow_ticket(sysid, type, rows_affected, data):
        # Set the ServiceNow Patch return endpoint
        updateurl = endpoint + '/' + sysid
        
        if type == 'UpdateTicket':
            # Sending Awaiting Feedback back to ServiceNow API
            if data != " ":
                output = 'Automation Tool is working on this request.Please wait for the update'
                response = requests.patch(updateurl, auth=(user, password), headers=headers, data="{'state':'16', 'work_notes':'" +output+ "'}")
            else:
                output = 'Failure: Plese contact source team via email fredlud@example.com'
                response = requests.patch(updateurl, auth=(user, password), headers=headers, data="{'state':'16','work_notes':'" +output+ "'}")
            if response.status_code != 200:
                print('Error updating incident record: {}'.format(response.text))
                exit()

            # Print final output
            print(output)
        else:
            # Send Closing status back to ServiceNow API
            if rows_affected > 0:
                output = 'Success: {} - Account Status changed to Active. {} row updated.'.format(userid, rows_affected)
                response = requests.patch(updateurl, auth=(user, password), headers=headers, data="{'assigned_to':'Fred Luddy', 'assignment_group':'Database', 'state':'3', 'work_notes':'" +output+ "'}")
            else:
                output = 'Failure: {} - User is already in active state. Nothing Updated.'.format(userid)
                response = requests.patch(updateurl, auth=(user, password), headers=headers, data="{'work_notes':'" +output+ "'}")

            if response.status_code != 200:
                print('Error updating incident record: {}'.format(response.text))
                exit()

            # Print final output
            print(output)

    def my_sql_update(userid):
         # Set up MySQL database credentials
        db_host = 'localhost'
        db_user = 'root'
        db_password = 'myhomedb'
        db_name = 'mybase'
        db_port = '3306'
        status = 'Active' 
       # Connect to MySQL database and run query to update user_table
        cnx = mysql.connector.connect(host=db_host, port=db_port, user=db_user, password=db_password, database=db_name)
        #print(cnx.is_connected()) - to check if connection is live
        cursor = cnx.cursor()
        query = '''
            UPDATE user
            SET status = %s
            WHERE username = %s
        '''
        params = (status, userid)
        cursor.execute(query, params)
        cnx.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        return rows_affected

if __name__ == "__main__":
        main()


   


