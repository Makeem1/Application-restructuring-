try:
    from urlparse import urljoin
except ImportError: 
    from urllib.parse import urljoin

from flask import request

def safe_url(target):
    '''This fuction help us to make sure that malicious attackers doesn't redirect our users to another domain'''
    return urljoin(request.host_url, target)
















    