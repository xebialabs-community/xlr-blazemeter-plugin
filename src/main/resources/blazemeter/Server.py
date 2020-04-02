#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
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