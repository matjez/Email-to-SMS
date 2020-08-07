import imaplib
import email
import webbrowser
import os

from email.header import decode_header
from twilio.rest import Client
from tinydb import TinyDB, Query


db = TinyDB('db.json')

if os.path.exists('data.txt'):
    data = {}
    f = open("data.txt","r")
    list_of_lines = f.readlines()

    for line in list_of_lines:
        line_splitted = line.replace("\n","").split("==")
        data[line_splitted[0]] = line_splitted[1]
    
    f.close()

max_number_of_messages = int(data["max_number_of_messages"])


def send_SMS(number,from_who,message,msg_id):
    global max_number_of_messages

    if data["followed_email"] in from_who:
        get_id = Query()
        email_id_in_db = db.search(get_id.id==msg_id)

        if len(email_id_in_db) == 0 and max_number_of_messages > 0:
            db.insert({'id': msg_id})

            print(number, from_who, message)

            client = Client(data["twillio_sid"], data["twillio_auth_token"])


            body = "Mail from {} ".format(from_who)

            length = 70-len(body)

            if length > 0:
                if len(message) > length:
                    body += message[:length]
                else:
                    body += message     

            print(body)

            max_number_of_messages -= 1

            print(max_number_of_messages, "messages left.")

            # zrobic sprawdzanie dlugosci smsa i dalej loopa 

            # message = client.messages \
            #                 .create(
            #                     body=message,
            #                     from_=data["SMS_header"],
            #                     to=data["phone_number_destintion"]
            #                 )

            # print(message.sid)

    else:
        return 


def update_status():

    imap = imaplib.IMAP4_SSL("imap.gmail.com")

    imap.login(data["email"], data["password"])

    status, messages = imap.select("INBOX")

    messages = int(messages[0])

    for i in range(messages, messages-int(data["number_of_emails_to_check"]), -1):

        res, msg = imap.fetch(str(i), "(RFC822)")

        for response in msg:
            if isinstance(response, tuple):
                
                msg = email.message_from_bytes(response[1])
                
                subject = decode_header(msg["Subject"])[0][0]
                if isinstance(subject, bytes):

                    subject = subject.decode("latin2")

                msg_id = msg.get("Message-ID")
                from_ = msg.get("From")

                if msg.is_multipart():
                    for part in msg.walk():

                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        
                        try:
                            body = part.get_payload(decode=True).decode("latin2")
                        except:
                            pass
                            
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            send_SMS(783621421,from_,body,msg_id)

                else:
                    content_type = msg.get_content_type()
                    body = msg.get_payload(decode=True).decode("latin2")
                    if content_type == "text/plain":
                        send_SMS(783621421,str(from_),body,msg_id)

    imap.close()
    imap.logout()            

print("Running...")

while True:
    x = input("Type y to refresh q to quit: ")
    if x == "y" or x == "Y":
        update_status()
    else: 
        break
