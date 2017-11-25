from flask.globals import _app_ctx_stack, _request_ctx_stack
from werkzeug.urls import url_parse
from werkzeug.exceptions import NotFound
from .exceptions import ValidationError
import string, time, math, random
from calendar import monthrange
from datetime import datetime, timedelta


def split_url(url, method='GET'):
    """Returns the endpoint name and arguments that match a given URL. In
    other words, this is the reverse of Flask's url_for()."""
    appctx = _app_ctx_stack.top
    reqctx = _request_ctx_stack.top
    if appctx is None:
        raise RuntimeError('Attempted to match a URL without the '
                           'application context being pushed. This has to be '
                           'executed when application context is available.')

    if reqctx is not None:
        url_adapter = reqctx.url_adapter
    else:
        url_adapter = appctx.url_adapter
        if url_adapter is None:
            raise RuntimeError('Application was not able to create a URL '
                               'adapter for request independent URL matching. '
                               'You might be able to fix this by setting '
                               'the SERVER_NAME config variable.')
    parsed_url = url_parse(url)
    if parsed_url.netloc is not '' and \
                    parsed_url.netloc != url_adapter.server_name:
        raise ValidationError('Invalid URL: ' + url)
    try:
        result = url_adapter.match(parsed_url.path, method)
    except NotFound:
        raise ValidationError('Invalid URL: ' + url)
    return result


def generate_code():
    code = '-'.join(map(str, random.sample(range(1, 1000), 3)))
    return code


def generate_username(names):
    names = names.split(" ")
    first_letter = names[0][0]
    three_letters_surname = names[-1][:3]
    number = '{:03d}'.format(random.randrange(1, 999))
    username = (first_letter + three_letters_surname + number)
    return username


def generate_email(names):
    names = names.split(" ")
    first_letter = names[0][0]
    three_letters_surname = names[-1][:3]
    number = '{:03d}'.format(random.randrange(1, 999))
    username = (first_letter + three_letters_surname + number)
    return username + "@getsave.io"


def uniqid_email(prefix='pwd-up', more_entropy=True):
    m = time.time()
    uniqid = '%8x%05x' % (math.floor(m), (m - math.floor(m)) * 1000000)
    if more_entropy:
        valid_chars = list(set(string.hexdigits.lower()))
        entropy_string = ''
        for i in range(0, 50, 1):
            entropy_string += random.choice(valid_chars)
        uniqid = uniqid + entropy_string
    uniqid = prefix + uniqid
    return uniqid


def monthdelta(d1, d2):
    delta = 0
    while True:
        mdays = monthrange(d1.year, d1.month)[1]
        d1 += timedelta(days=mdays)
        if d1 <= d2:
            delta += 1
        else:
            break
    return delta

