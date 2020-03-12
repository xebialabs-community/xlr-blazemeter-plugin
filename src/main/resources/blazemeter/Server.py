#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

from blazemeter.HttpRequest import HttpRequest

import logging

logging.basicConfig(filename='log/plugin.log',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

logging.debug("Server: begin")

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

# check response status code, if different than 200 exit with error code
if response.status != 200:
    raise Exception(
        "Failed to connect to Blazemeter Server. Status: %s" % response.status
    )

logging.debug("Server: end")
