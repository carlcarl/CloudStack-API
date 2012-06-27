#!/usr/bin/env python

# by carlcarl

import getopt
import sys
import hmac
import hashlib
import base64
import urllib


def formattedCmd(api, cmd):
    s = 'apiKey=' + api + '&' + cmd
    return s


def encypt(string, key):
    h = hmac.new(key, string, hashlib.sha1)
    return base64.b64encode(h.digest())


def formattedUrl(baseUrl, api, cmd, signature):
    url = baseUrl + '?' + formattedCmd(api, cmd) + '&' + urllib.urlencode({'signature': signature})
    return url


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'u:a:s:', ['help', 'output='])
    except getopt.GetoptError, err:
        print str(err)
        sys.exit(2)

    baseUrl = 'http://*.*.*.*:8080/client/api'
    cmd = api = secret = None

    for o, a in opts:
        if o == '-u':
            cmd = a
        elif o == '-a':
            api = a
        elif o == '-s':
            secret = a
        else:
            assert False, 'unhandled option'

    newCmd = formattedCmd(api, cmd).lower()
    signature = encypt(newCmd, secret)
    url = formattedUrl(baseUrl, api, cmd, signature)

    print '\n' + url

if __name__ == '__main__':
    main()
