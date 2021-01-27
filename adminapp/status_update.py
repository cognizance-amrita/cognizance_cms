from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime
import psycopg2
from datetime import date 
from datetime import timedelta 

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def get_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
   
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service=build('gmail', 'v1', credentials=creds)
    return service

# Starting of main code part 
def get_update():

    # accessing the threads from mail 
    results = get_service().users().messages().list(userId='me', labelIds='INBOX').execute()
    messages = results.get('messages',[])
    
    values=[]
    for message in messages:
         msg = get_service().users().messages().get(userId='me', id=message['id']).execute()
         time=int(msg['internalDate'])
         timestamp=datetime.datetime.fromtimestamp(time/1000)      # it's in epoch time so we are converting it using datetime module
         name=msg['payload']['headers']
         mailname = None
         for i in range(0,len(name)):
             if name[i]['name']=='From':                  # getting the From address of the mail from headers field
                 mailname=name[i]['value']
                 break
         cont=msg['payload']['headers']
         content = None
         for i in range(0,len(name)):
             if cont[i]['name']=='Subject':                  # getting the subject of the mail from headers field
                 content=name[i]['value']
                 break            
         values.append((str(timestamp), mailname, content))
    return values
    
def filter_update(sdate,mem_mail):
    data = get_update()
    d = sdate + timedelta(days = 1) 
    e = '18:00:00'
    f = '06:00:00'
    res=[]
    for i in range(len(data)):
    	a,b = data[i][0].split()
    	l = data[i][1].split()
    	mail = l[-1]
    	mail = str(mail[1:-1])
    	if mail in mem_mail: 
    	    if a == str(sdate):
    	        if b > e :
    	    	    res.append((data[i][0],mail))
    	    elif a == str(d):
    	        if b < f :
    	            res.append((data[i][0],mail))
    return res
        


