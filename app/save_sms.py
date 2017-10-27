import nexmo

client = nexmo.Client(key='de087b65', secret='9c629de08d20b047')


def save_sms(to, text):
    client.send_message({
      'from': 'Save',
      'to': to,
      'text': text
    })
