import re
import urllib
import logging
import traceback

from java.lang import Integer
from java.lang import String
from java.util import Arrays

from org.apache.commons.codec.binary import Base64
from org.apache.http import HttpHost
from org.apache.http.auth import AuthScope, NTCredentials, UsernamePasswordCredentials
from org.apache.http.client.config import AuthSchemes, RequestConfig
from org.apache.http.client.methods import HttpGet, HttpHead, HttpPost, HttpPut, HttpDelete, HttpPatch
from org.apache.http.client.protocol import HttpClientContext
from org.apache.http.impl.client import BasicCredentialsProvider, HttpClientBuilder, HttpClients
from org.apache.http.util import EntityUtils
from org.apache.http.entity import StringEntity
from org.apache.http.protocol import BasicHttpContext

from com.xebialabs.xlrelease.domain.configuration import HttpConnection
from xlrelease.HttpResponse import HttpResponse


class HttpRequest:
    def __init__(self, params, username = None, password = None, domain = None):
        """
        Builds an HttpRequest

        :param params: an <a href="/jython-docs/#!/_PROD_VERSION_/service/com.xebialabs.xlrelease.domain.configuration.HttpConnection">HttpConnection</a>
        :param username: the username
            (optional, it will override the credentials defined on the <a href="/jython-docs/#!/_PROD_VERSION_/service/com.xebialabs.xlrelease.domain.configuration.HttpConnection">HttpConnection</a> object)
        :param password: an password
            (optional, it will override the credentials defined on the <a href="/jython-docs/#!/_PROD_VERSION_/service/com.xebialabs.xlrelease.domain.configuration.HttpConnection">HttpConnection</a> object)
        :param domain: the Ntlm authentication domain
            (optional, and only used if Ntlm authentication enabled, it will override the credentials defined on the <a href="/jython-docs/#!/_PROD_VERSION_/service/com.xebialabs.xlrelease.domain.configuration.HttpConnection">HttpConnection</a> object)
        """

        if params.get('authenticationMethod') == "PAT":
            if not params['username']:
                params['username'] = "dummy"

            if username is not None and not username:
                username = "dummy"

        self.params = HttpConnection(params)
        self.shared_domain = params.get('domain')
        self.username = username
        self.password = password
        self.domain = domain
        self.authentication = params.get('authenticationMethod')

    def doRequest(self, **options):
        """
        Performs an HTTP Request

        :param options: A keyword arguments object with the following properties :
            method: the HTTP method : 'GET', 'PUT', 'POST', 'DELETE', 'PATCH'
                (optional: GET will be used if empty)
            context: the context url
                (optional: the url on <a href="/jython-docs/#!/_PROD_VERSION_/service/com.xebialabs.xlrelease.domain.configuration.HttpConnection">HttpConnection</a> will be used if empty)
            body: the body of the HTTP request for PUT & POST calls
                (optional: an empty body will be used if empty)
            contentType: the content type to use
                (optional, no content type will be used if empty)
            headers: a dictionary of headers key/values
                (optional, no headers will be used if empty)
        :return: an <a href="/jython-docs/#!/_PROD_VERSION_/service/HttpResponse.HttpResponse">HttpResponse</a> instance
        """
        request = self.buildRequest(
            options.get('method', 'GET'),
            options.get('context', ''),
            options.get('body', ''),
            options.get('contentType', None),
            options.get('headers', None))
        return self.executeRequest(request)


    def get(self, context, **options):
        """
        Performs an HTTP GET Request

        :param context: the context url
        :param options: the options keyword argument described in doRequest()
        :return: an <a href="/jython-docs/#!/_PROD_VERSION_/service/HttpResponse.HttpResponse">HttpResponse</a> instance
        """
        options['method'] = 'GET'
        options['context'] = context
        return self.doRequest(**options)


    def head(self, context, **options):
        """
        Performs an HTTP HEAD Request

        :param context: the context url
        :param options: the options keyword argument described in doRequest()
        :return: an <a href="/jython-docs/#!/_PROD_VERSION_/service/HttpResponse.HttpResponse">HttpResponse</a> instance
        """
        options['method'] = 'HEAD'
        options['context'] = context
        return self.doRequest(**options)


    def put(self, context, body, **options):
        """
        Performs an HTTP PUT Request

        :param context: the context url
        :param body: the body of the HTTP request
        :param options: the options keyword argument described in doRequest()
        :return: an <a href="/jython-docs/#!/_PROD_VERSION_/service/HttpResponse.HttpResponse">HttpResponse</a> instance
        """
        options['method'] = 'PUT'
        options['context'] = context
        options['body'] = body
        return self.doRequest(**options)


    def post(self, context, body, **options):
        """
        Performs an HTTP POST Request

        :param context: the context url
        :param body: the body of the HTTP request
        :param options: the options keyword argument described in doRequest()
        :return: an <a href="/jython-docs/#!/_PROD_VERSION_/service/HttpResponse.HttpResponse">HttpResponse</a> instance
        """
        options['method'] = 'POST'
        options['context'] = context
        options['body'] = body
        return self.doRequest(**options)


    def delete(self, context, **options):
        """
        Performs an HTTP DELETE Request

        :param context: the context url
        :param options: the options keyword argument described in doRequest()
        :return: an <a href="/jython-docs/#!/_PROD_VERSION_/service/HttpResponse.HttpResponse">HttpResponse</a> instance
        """
        options['method'] = 'DELETE'
        options['context'] = context
        return self.doRequest(**options)

    def patch(self, context, body, **options):
        """
        Performs an HTTP PATCH Request

        :param context: the context url
        :param body: the body of the HTTP request
        :param options: the options keyword argument described in doRequest()
        :return: an <a href="/jython-docs/#!/_PROD_VERSION_/service/HttpResponse.HttpResponse">HttpResponse</a> instance
        """
        options['method'] = 'PATCH'
        options['context'] = context
        options['body'] = body
        return self.doRequest(**options)

    def buildRequest(self, method, context, body, contentType, headers):
        url = self.quote(self.createPath(self.params.getUrl(), context))

        method = method.upper()

        if method == 'GET':
            request = HttpGet(url)
        elif method == 'HEAD':
            request = HttpHead(url)
        elif method == 'POST':
            request = HttpPost(url)
            request.setEntity(StringEntity(body))
        elif method == 'PUT':
            request = HttpPut(url)
            request.setEntity(StringEntity(body))
        elif method == 'DELETE':
            request = HttpDelete(url)
        elif method == 'PATCH':
            request = HttpPatch(url)
            request.setEntity(StringEntity(body))
        else:
            raise Exception('Unsupported method: ' + method)

        request.addHeader('Content-Type', contentType)
        request.addHeader('Accept', contentType)
        self.setCredentials(request)
        self.setProxy(request)
        self.setHeaders(request, headers)

        return request


    def createPath(self, url, context):
        url = re.sub('/*$', '', url)
        if context is None:
            return url
        elif context.startswith('/'):
            return url + context
        else:
            return url + '/' + context

    def quote(self, url):
        return urllib.quote(url, ':/?&=%')


    def set_basic_credentials(self, request):
        credentials = self.get_credentials()
        encoding = Base64.encodeBase64String(String(credentials["username"] + ':' + credentials["password"]).getBytes('ISO-8859-1'))
        request.addHeader('Authorization', 'Basic ' + encoding)

    def set_pat_credentials(self, request):
        credentials = self.get_credentials()
        encoding = Base64.encodeBase64String(String(':' + credentials["password"]).getBytes('ISO-8859-1'))
        request.addHeader('Authorization', 'Basic ' + encoding)

    def get_ntlm_client(self):
        if self.params.proxyUsername and self.params.proxyPassword:
            proxy = HttpHost(self.params.getProxyHost(), int(self.params.getProxyPort()))
            request_config = RequestConfig.custom().setTargetPreferredAuthSchemes(Arrays.asList(AuthSchemes.NTLM)).setProxy(proxy).build()
            creds_provider = self.get_proxy_credentials_provider()
            http_client = HttpClients.custom().setDefaultRequestConfig(request_config).setDefaultCredentialsProvider(creds_provider).build()
        else:
            request_config = RequestConfig.custom().setTargetPreferredAuthSchemes(Arrays.asList(AuthSchemes.NTLM)).build()
            http_client = HttpClients.custom().setDefaultRequestConfig(request_config).build()
        return http_client

    def get_default_client(self):
        if self.params.proxyUsername and self.params.proxyPassword:
            creds_provider = self.get_proxy_credentials_provider()
            http_client = HttpClients.custom().setDefaultCredentialsProvider(creds_provider).build()
        else:
            http_client = HttpClients.custom().build()
        return http_client


    def setCredentials(self, request):
        if self.username:
            username = self.username
            password = self.password
        elif self.params.getUsername():
            username = self.params.getUsername()
            password = self.params.getPassword()
        else:
            return

        encoding = Base64.encodeBase64String(String(username + ':' + password).getBytes('ISO-8859-1'))
        request.addHeader('Authorization', 'Basic ' + encoding)


    def get_credentials(self):
        if self.username:
            username = self.username
            password = self.password
            domain = self.domain
        elif self.params.getUsername():
            username = self.params.getUsername()
            password = self.params.getPassword()
            domain = self.shared_domain
        else:
            return
        return {'username': username, 'password': password, 'domain': domain}

    def get_proxy_credentials_provider(self):
        credentials = UsernamePasswordCredentials(self.params.proxyUsername, self.params.proxyPassword)
        auth_scope = AuthScope(self.params.proxyHost, Integer.valueOf(self.params.proxyPort))
        creds_provider = BasicCredentialsProvider()
        creds_provider.setCredentials(auth_scope, credentials)
        return creds_provider

    def setProxy(self, request):
        if not self.params.getProxyHost():
            return

        proxy = HttpHost(self.params.getProxyHost(), int(self.params.getProxyPort()))
        config = RequestConfig.custom().setProxy(proxy).build()
        request.setConfig(config)


    def setHeaders(self, request, headers):
        if headers:
            for key in headers:
                request.setHeader(key, headers[key])


    def executeRequest(self, request):
        logging.debug('HttpRequest: begin')
        client = None
        response = None
        try:
            local_context = BasicHttpContext()
            if self.authentication == "Ntlm":
                logging.debug('HttpRequest: local_context: ntlm')
                credentials = self.get_credentials()
                client = self.get_ntlm_client()
                credentials_provider = BasicCredentialsProvider()
                credentials_provider.setCredentials(AuthScope.ANY, NTCredentials(credentials["username"], credentials["password"], None, credentials["domain"]))
                local_context.setAttribute(HttpClientContext.CREDS_PROVIDER, credentials_provider)
            elif self.authentication == "PAT":
                logging.debug('HttpRequest: local_context: pat')
                client = self.get_default_client()
                self.set_pat_credentials(request)
            elif self.authentication == "Basic":
                logging.debug('HttpRequest: local_context: basic')
                client = self.get_default_client()
                self.set_basic_credentials(request)
            elif self.params.proxyUsername and self.params.proxyPassword:
                logging.debug('HttpRequest: local_context: proxy')
                credentials = UsernamePasswordCredentials(self.params.proxyUsername, self.params.proxyPassword)
                auth_scope = AuthScope(self.params.proxyHost, Integer.valueOf(self.params.proxyPort))
                creds_provider = BasicCredentialsProvider()
                creds_provider.setCredentials(auth_scope, credentials)
                client = HttpClientBuilder.create().setDefaultCredentialsProvider(creds_provider).build()
            else:
                logging.debug('HttpRequest: local_context: default')
                client = HttpClients.createDefault()

            logging.debug('HttpRequest: client.execute')
            response = client.execute(request, local_context)
            logging.debug('HttpRequest: response type: %s' % type(response))
            status = response.getStatusLine().getStatusCode()
            logging.debug('HttpRequest: status %s, getting entity' % status)
            entity = response.getEntity()
            logging.debug('HttpRequest: entity toString')
            result = EntityUtils.toString(entity, "UTF-8") if entity else None
            logging.debug('HttpRequest: result: %s, getting headers' % result)
            headers = response.getAllHeaders()
            logging.debug('HttpRequest: consuming entity')
            EntityUtils.consume(entity)

            logging.debug('HttpRequest: returning HttpResponse')
            return HttpResponse(status, result, headers)

        except Exception as e:
            logging.error('Exception...')
            logging.error(e)
            logging.error(traceback.format_exc())
            raise

        finally:
            logging.debug('HttpRequest: finally: close response')
            if response:
                response.close()
            logging.debug('HttpRequest: finally: close client')
            if client:
                client.close()
            logging.debug('HttpRequest: finally: done')
