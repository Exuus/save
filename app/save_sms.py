import nexmo

client = nexmo.Client(key='de087b65', secret='9c629de08d20b047')


def save_sms(to, text):
    return client.send_message({
      'from': 'Save',
      'to': to,
      'text': text
    })


def new_member_sms(sg_name, user_name, to):
    text = user_name + '+Welcome+to+Save.You+have+been+added+to' + sg_name + '+group'
    return client.send_message({
        'from': 'Save',
        'to': to,
        'text': text
    })

