#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import sys
import time
import base64
import random
import json

from ast import literal_eval
from blazemeter.common import (call_url, encode_multipart)

# Initialize variables
base_url = server.get('url').strip('/')
contents = ''

# Make sure all the required paramaters are set
if not base_url.strip():
    print 'FATAL: Input error! Server configuration url undefined\n'
    sys.exit(101)

if not keyId.strip():
    print 'FATAL: Input error! Parameter keyId undefined\n'
    sys.exit(102)

if not secret.strip():
    print 'FATAL: Input error! Parameter secret undefined\n'
    sys.exit(103)

if not test.strip():
    print 'FATAL: Input error! Parameter test undefined\n'
    sys.exit(104)

if not filename.strip():
    print 'FATAL: Input error! Parameter filename undefined\n'
    sys.exit(105)

if not testData:
    print 'FATAL: Input error! Parameter testData undefined\n'
    sys.exit(106)

print 'BlazeMeter test data upload started\n'

# Write the data to a string
try:
    for r in testData:
        row = literal_eval(r)
        contents += ','.join(map(str, row)) + '\n'
except Exception as error:
    print 'FATAL: The test data is in the wrong format!\n'
    print 'Example: ["(\'Header1\', \'Header2\')", "(\'Value1\', \'Value2\')"]\n'
    sys.exit(107)

# Encode multipart form data
files = {'file': {'filename': filename, 'content': contents}}
url_data, url_headers = encode_multipart({}, files)

# Add headers
base64string = base64.encodestring('%s:%s' % (keyId, secret)).replace('\n', '')
url_headers['Authorization'] = 'Basic %s' % base64string

# Upload the test data
upload_url = '%s/tests/%s/files' % (base_url, test)
data = call_url('post', upload_url, url_data, url_headers)

if 'updated' in data.get('result') and data.get('result').get('updated') == True:
    print 'BlazeMeter file upload for test %s completed **successfully**\n' % test
    sys.exit(0)    
        
print 'FATAL: BlazeMeter upload for test %s **failed**:\n' % test
print '```'
print json.dumps(data)
print '```'
sys.exit(1)