#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
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
