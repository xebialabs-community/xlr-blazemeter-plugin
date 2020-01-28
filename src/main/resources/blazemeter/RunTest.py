#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import json
import sys
import time
import base64
from blazemeter.common import (call_url, encode_multipart)

# Initialize variables
app_url = ''
data = ''
project = ''
account = ''
headers = {}

# Make sure all the required paramaters are set
if not server and server.get('url'):
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

if not pollingInterval:
    print 'FATAL: Input error! Parameter pollingInterval undefined\n'
    sys.exit(105)

print 'BlazeMeter test execution started\n'

# Add headers
base64string = base64.encodestring('%s:%s' % (keyId, secret)).replace('\n', '')
headers['Authorization'] = 'Basic %s' % base64string
headers['Content-Type'] = 'application/json'

# Start the test
base_url = server.get('url').strip('/')
serverProxyHost = server.get('proxyHost')
serverProxyPort = server.get('proxyPort')
serverProxyUsername = server.get('proxyUsername')
serverProxyPassword = server.get('proxyPassword')
start_test_url = '/api/v4/tests/%s/start' % (test)
data = call_url('post', {}, base_url, start_test_url, keyId, secret, serverProxyHost, serverProxyPort, serverProxyUsername, serverProxyPassword)
sessions = data.get('result').get('sessionsId')

print 'The following sessions were successfully started: %s\n' % ', '.join(sessions)

# Retrieve the master id from the first session
session_url = '/api/v4/sessions/%s' % (sessions[0])
data = call_url('get', None, base_url, session_url, keyId, secret, serverProxyHost, serverProxyPort, serverProxyUsername, serverProxyPassword)
master = data.get('result').get('masterId')
project = data.get('result').get('projectId')

# Update the test with a custom note
master_url = '/api/v4/masters/%s' % (master)
if note and note.strip():
    note_json = {"note": note}
    data = call_url('patch', json.dumps(note_json), base_url, master_url, keyId, secret, serverProxyHost, serverProxyPort, serverProxyUsername, serverProxyPassword)
    if not data.get('error'):
        print 'Successfully updated the notes for this test\n'

# Monitor the progress of the sessions
count = 1
while True:
    for session in sessions[:]:
        print 'Monitoring session [%s] progress #%d\n' % (session, count)
        session_status_url = '/api/v4/sessions/%s/status' % (session)
        count += 1
        data = call_url('get', None, base_url, session_status_url, keyId, secret, serverProxyHost, serverProxyPort, serverProxyUsername, serverProxyPassword)
        if data.get('result').get('status') == "ENDED":
            if 'errors' in data.get('result') and data.get('result').get('errors'):
                error = data.get('result').get('errors')[0]
                print 'FATAL: Session [%s] terminated with error code %s!\n' % (session, error.get('code'))
                sys.exit(106)
            else:
                sessions.remove(session)
    if not sessions:
        break
    time.sleep(pollingInterval)

# Retrieve the account information to build a url in order to view the reports
account_url = '/api/v4/accounts'
data = call_url('get', None, base_url, account_url, keyId, secret, serverProxyHost, serverProxyPort, serverProxyUsername, serverProxyPassword)
result = data.get('result')[0]
if result and 'id' in result:
    account = result.get('id')
    app_url = result.get('appUrl')
    print 'Test report summary URL: %s/app/#/accounts/%s/workspaces/%s/projects/%s/masters/%s/summary\n' % (app_url, account, workspace, project, master)

# Review the test report
data = call_url('get', None, base_url, master_url, keyId, secret, serverProxyHost, serverProxyPort, serverProxyUsername, serverProxyPassword)
if 'passed' in data.get('result') and data.get('result').get('passed') == False:
    print 'BlazeMeter test %s **failed**:\n' % test
    print '```'
    print json.dumps(data)
    print '```'
    sys.exit(1)

# If we got this far it means that the test was successful!
print 'BlazeMeter test %s completed **successfully**\n' % test
sys.exit(0)