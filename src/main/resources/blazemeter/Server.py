#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

# get the configuration properties from the UI
params = {
    'url': configuration.url,
    'username': configuration.username,
    'password': configuration.password,
    'proxyHost': configuration.proxyHost,
    'proxyPort': configuration.proxyPort,
    'proxyUsername': configuration.proxyUsername,
    'proxyPassword': configuration.proxyPassword
}
# make a http request call to the server - access the user api in this test
response = HttpRequest(params).get('/api/v4/user', contentType='application/json')

# some failures in the org.apache.http.client library can raise silent exceptions.  In that case 'response' will be None.
if not response:
    raise Exception(
        "No response from Blazemeter Server.  Possible SSL negotiation failure."
    )

# check response status code, if different than 200 exit with error code
if response.status != 200:
    raise Exception(
        "Failed to connect to Blazemeter Server. Status: %s" % response.status
    )