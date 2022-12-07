# Email-to-SMS
 SMS notification about received email from specific address (with twilio).
 
 # Requirements
 - Python 3+
 - requirements.txt
 - Twilio account
 
# Configuration
 
 1. Create account (Free or Premium) on twilio.com and enable your phone number
 2. First you have to setup data.txt file. (Examples and explanation below)
 3. Run run.py file.
 
 
- email==example@test.com  -  Your email address
- password==qwerty123  -  Your email address password
- followed_email==myemail@test.com  -  Email address that will be 'tracked'
- imap_server==imap.gmail.com  -  Imap server addres(default for gmail)
- number_of_emails_to_check==1  -  Number of emails to get from your mailbox
- max_number_of_messages==5  -  Max number of messages sent to your phone (to prevent spam)
- max_length_of_sms==32  -  Maximum length of SMS message
- interval==30  -  Interval[s] between checking for new messages
- source_phone_number==+48987654321  -  Your twilio phone number
- phone_number_destintion==+48123456789  -  Destination phone number
- twillio_sid==some_id  -  Twilio sid
- twillio_auth_token==some_auth_token  -  Twilio authorization token


If you want to use it on your private email I recommend you creating another account and redirect mails from one mailbox to another. If you use gmail account first you have to enable less secure apps. 

