#!/usr/bin/env python3
import os
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient
import json

from config import *



def SendDynamic(TO_EMAILS, content):
    """ Send a dynamic email to a list of email addresses

    :returns API response code
    :raises Exception e: raises an exception """
    # create Mail object and populate
    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=TO_EMAILS)
    
    # print(json.dumps(content))
    # exit()
    # pass custom values for our HTML placeholders
    message.dynamic_template_data = {
        "news": content
    }
    
    message.template_id = TEMPLATE_ID
    # create our sendgrid client object, pass it our key, then send and return our response objects
    # print(os.environ.get('SENDGRID_API_KEY'))
    # exit()
    try:
        sg = SendGridAPIClient(TOKEN)
        response = sg.send(message)
        code, body, headers = response.status_code, response.body, response.headers
        print(f"Response code: {code}")
        print(f"Response headers: {headers}")
        print(f"Response body: {body}")
        print("Dynamic Messages Sent!")
    except Exception as e:
        print("Error: {0}".format(e))
        return str(response.status_code)


# if __name__ == "__main__":
#     SendDynamic()