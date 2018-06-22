#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import json
import sys
import urllib2
import ssl
import time
import base64

from blazemeter.common import (call_url, encode_multipart)

# Initialize variables
base_url = server.get('url').strip('/')
app_url = ''
data = ''
project = ''
account = ''
headers = {}

# Make sure all the required paramaters are set
if not base_url.strip():
    print 'Input error!\n'
    print 'Reason: Server configuration url undefined\n'
    sys.exit(101)

if not keyId.strip():
    print 'Input error!\n'
    print 'Reason: Parameter keyId undefined\n'
    sys.exit(102)

if not secret.strip():
    print 'Input error!\n'
    print 'Reason: Parameter secret undefined\n'
    sys.exit(103)

if not test.strip():
    print 'Input error!\n'
    print 'Reason: Parameter test undefined\n'
    sys.exit(104)

if not pollingInterval:
    print 'Input error!\n'
    print 'Reason: Parameter pollingInterval undefined\n'
    sys.exit(105)

print 'BlazeMeter test execution started\n'

# Add headers
base64string = base64.encodestring('%s:%s' % (keyId, secret)).replace('\n', '')
headers['Authorization'] = 'Basic %s' % base64string
headers['Content-Type'] = 'application/json'

# Start the test
start_test_url = '%s/tests/%s/start' % (base_url, test)
data = call_url('post', start_test_url, {}, headers)
session = data.get('result').get('sessionsId')[0]

# Monitor the progress of the session
print 'The following session was successfully started: %s\n' % session
session_status_url = '%s/sessions/%s/status' % (base_url, session)
count = 1
while True:
    print 'Monitoring session progress #%d\n' % count
    data = call_url('get', session_status_url, None, headers)
    if data.get('result').get('status') == "ENDED":
        if 'errors' in data.get('result') and data.get('result').get('errors'):
            error = data.get('result').get('errors')[0]
            print 'Session %s error!\n' % error.get('code')
            print 'Reason: %s\n' % error.get('message')
            sys.exit(106)
        else:
            break
    count += 1   
    time.sleep(pollingInterval)

# Retrieve the master id from the session
session_url = '%s/sessions/%s' % (base_url, session)
data = call_url('get', session_url, None, headers)
master = data.get('result').get('masterId')
project = data.get('result').get('projectId')

# Update the test with a custom note, when available
master_url = '%s/masters/%s' % (base_url, master)
if note.strip():
    note_json = {"note": note}
    data = call_url('patch', master_url, json.dumps(note_json), headers)
    if not data.get('error'):
        print 'Successfully updated the notes for this test\n'

# Retrieve the various elements to build a url in order to view the reports
account_url = '%s/accounts' % base_url
data = call_url('get', account_url, None, headers)
result = data.get('result')[0]
if result and 'id' in result:
    account = result.get('id')
    app_url = result.get('appUrl')
    print 'Test report summary URL: %s/app/#/accounts/%s/workspaces/%s/projects/%s/masters/%s/summary\n' % (app_url, account, workspace, project, master)

# Review the test report
data = call_url('get', master_url, None, headers)
if 'passed' in data.get('result') and data.get('result').get('passed') == False:
    print 'BlazeMeter test %s **failed**\n' % test
    print '```'
    print json.dumps(data)
    print '```'
    sys.exit(1)

# If we got this far it means that the test was successful!
print 'BlazeMeter test %s completed **successfully**\n' % test
print '```'
print json.dumps(data)
print '```'
sys.exit(0)