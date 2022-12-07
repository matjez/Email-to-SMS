import imaplib
import email
import os
import time

from twilio.rest import Client
from tinydb import TinyDB, Query


if os.path.exists('config.txt'):
    
    data = {}
    f = open("config.txt", "r")
    list_of_lines = f.readlines()

    for line in list_of_lines:
        line_splitted = line.replace("\n", "").split("==")
        data[line_splitted[0]] = line_splitted[1]

    f.close()

max_number_of_messages = int(data["max_number_of_messages"])
loops_without_sms = int(data["number_of_emails_to_check"])


def send_sms(from_who, message, msg_id):
    global max_number_of_messages, loops_without_sms 

    if data["followed_email"] in from_who:

        db = TinyDB('db.json')
        get_id = Query()
        email_id_in_db = db.search(get_id.id == msg_id)

        if len(email_id_in_db) == 0 and max_number_of_messages > 0:
            db.insert({'id': msg_id})

            if loops_without_sms > 0:
                loops_without_sms -= 1

            else:

                client = Client(data["twillio_sid"], data["twillio_auth_token"])
                body = "{} {}".format(from_who, message)
                length = int(data["max_length_of_sms"])-len(body)

                if length < 0:
                    body = body[:int(data["max_length_of_sms"])]
                    
                max_number_of_messages -= 1
 
                print(body, max_number_of_messages, "messages left.")
                
                message = client.messages \
                                .create(
                                    body=body,
                                    from_=data["source_phone_number"],
                                    to=data["phone_number_destintion"]
                                       )
                            
                print("SMS sent to {}.".format(data["phone_number_destintion"]))

        else:
            loops_without_sms -= 1 

    else:
        return 


def update_status():

    imap = imaplib.IMAP4_SSL(data["imap_server"])
    imap.login(data["email"], data["password"])

    status, messages = imap.select("INBOX")
    messages = int(messages[0])

    for i in range(messages, messages-int(data["number_of_emails_to_check"]), -1):

        res, msg = imap.fetch(str(i), "(RFC822)")

        for response in msg:
            if isinstance(response, tuple):
                
                msg = email.message_from_bytes(response[1])
                subject = email.header.decode_header(msg["Subject"])[0][0]

                if isinstance(subject, bytes):
                    subject = subject.decode("latin2")

                msg_id = msg.get("Message-ID")
                msg_from = msg.get("From")

                if msg.is_multipart():
                    for part in msg.walk():

                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        
                        try:
                            body = part.get_payload(decode=True).decode("latin2")
                        except:
                            pass
                        
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            send_sms(msg_from, body, msg_id)

                else:
                    content_type = msg.get_content_type()
                    body = msg.get_payload(decode=True).decode("latin2")

                    if content_type == "text/plain":
                        send_sms(str(msg_from), body, msg_id)

    imap.close()
    imap.logout()            


print("Running...\n")

while True:
    time.sleep(int(data["interval"]))
    update_status()
