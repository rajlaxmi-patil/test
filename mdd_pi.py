# -*- coding: utf-8 -*-
import smtplib
import imaplib, email 
from email.mime.text import MIMEText
from email.header import Header
import unicodedata
import re
import os
import time
import sys
import threading
import pdb

def sendMail(subject, message):

  # Python code to illustrate Sending mail from  
  # your Gmail account  
  
  # creates SMTP session 
  s = smtplib.SMTP('smtp.gmail.com', 587) 
  
  # start TLS for security 
  s.starttls() 
  
  # Authentication 
  s.login("oscmdreceiver@gmail.com","dsu@12345") 
  
  msg = MIMEText(message, _charset="UTF-8")
  msg['Subject'] = Header(subject, "utf-8")
  
  # sending the mail 
  s.sendmail("oscmdreceiver@gmail.com", "oscmdsender@gmail.com", msg.as_string()) 
  #s.sendmail("oscmdreceiver@gmail.com", "shekhar.biradar@gmail.com", msg.as_string()) 
  
  # terminating the session 
  s.quit() 
  
  
  
def receiveMail():
  #python code to receive a mail
  user = 'oscmdreceiver@gmail.com'
  password = 'dsu@12345'
  imap_url = 'imap.gmail.com'

 
  # Function to search for a key value pair 
  def search(con):
      result, data = con.search(None, "(UNSEEN)", '(SUBJECT "oscmd")' )
      return data 

  # Function to get the list of emails under this label 
  def get_emails(result_bytes): 
    msgs = [] # all the email data are pushed inside an array 
    for num in result_bytes[0].split(): 
      typ, data = con.fetch(num, '(RFC822)') 
      msgs.append(data) 
    return msgs 

  # this is done to make SSL connnection with GMAIL 
  con = imaplib.IMAP4_SSL(imap_url) 

  # logging the user in 
  con.login(user, password) 

  # calling fuction to check for email under this label 
  con.select('Inbox') 

  # fetching emails from this user "xyz@gmail.com" 
  msgs = get_emails(search(con)) 

 
  # Finding the required content from our msgs 
  # User can make custom changes in this part to 
  # fetch the required content he / she needs 

  # printing them by the order they are displayed in your gmail 
  for msg in msgs[::-1]: 
    #pdb.set_trace()
    for sent in msg: 
      if type(sent) is tuple:

        # encoding set as utf-8
        #content = str(sent[1], 'utf-8')
        content = str(sent[1])
        data = str(content) 

        # Handling errors related to unicodenecode 
        try: 
          indexstart = data.find("ltr") 
          data2 = data[indexstart + 5: len(data)] 
          indexend = data2.find("</div>") 

          # printtng the required content which we need 
          # to extract from our email i.e our body  
          b = email.message_from_string(data2[0: indexend])
          if b.is_multipart():
            for payload in b.get_payload():
              cmd = payload.get_payload()
              print("Received mail", cmd)
              #cmd = re.findall(r'\$(.*?)\$', payload.get_payload())
              return cmd.replace("\r\n","")
          

        except UnicodeEncodeError as e: 
          pass
  return 0


def main():
    #Daemon creation which checks mail
    print("Starting DNS Defender",len(sys.argv))

    file = open("/var/log/pihole.log","r")
    while 1:
    	where = file.tell()
    	line = file.readline()
    	if not line:
            time.sleep(1)
            file.seek(where)
        else:
           if "query[A]" in line:
	      domain = line.split(" ")[5]
              print domain # already has newline
    	      sendMail("mdd",domain)
              #exit(0)

main()
