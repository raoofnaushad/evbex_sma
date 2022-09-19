from send_email import *

from utils import *



def send_email():

    TO_EMAILS = get_subscribers_mongo()
    data = get_data_from_mongo()

    SendDynamic(TO_EMAILS, data)


    # for each in TO_EMAILS:

if __name__ == "__main__":
    send_email()