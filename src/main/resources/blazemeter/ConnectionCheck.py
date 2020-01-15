#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import base64
from blazemeter.common import (call_url, encode_multipart)

# Initialize variables
user_url = ''
data = ''
headers = {}

# Add headers
base64string = base64.encodestring('%s:%s' % (configuration.api_key_id, configuration.api_key_secret)).replace('\n', '')
headers['Authorization'] = 'Basic %s' % base64string
headers['Content-Type'] = 'application/json'

# Call the user api to see if we can make a connection to the server
user_url = '%s/user' % configuration.url
data = call_url('get', user_url, None, headers)
# If we don't throw an error in common.py, we are good to go.  All error handling is done in common.py
