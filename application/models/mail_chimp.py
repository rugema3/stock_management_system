api_key = 'md-r9nrL8uoJOn5hBu7DOnmZw'

import mailchimp_transactional as MailchimpTransactional
from mailchimp_transactional.api_client import ApiClientError

mailchimp = MailchimpTransactional.Client(api_key)
message = {
    "from_email": "arugema@remmittance.com",
    "subject": "Reset paswsword",
    "text": "this is an email sent from mail chimp api. I am trying to test if it works.",
    "to": [
      {
        "email": "rugema61@gmail.com",
        "type": "to"
      }
    ]
}

def run():
  try:
    response = mailchimp.messages.send({"message":message})
    print('API called successfully: {}'.format(response))
  except ApiClientError as error:
    print('An exception occurred: {}'.format(error.text))

run()
