# GlobalNOC WSC

WSC is a client implementation of the GlobalNOC Web Service calling convention.

You can use this library to interface with GlobalNOC Web Services.

## Features

- Authentication
  - HTTP Basic
  - Shibboleth password-based ECP
- GlobalNOC style service discovery
- POST only. GET is not supported.

## Getting Started

1. Install library
2. ...
3. Profit

## API Example

```python
from globalnoc import wsc

client = wsc.WSC()
client.username = 'exampleuser'
client.password = 'examplepassword'

client.url = 'https://example.grnoc.iu.edu/something/test.cgi'

resp = client.add_the_thing(something = "a string of text here", somethingelse = [1, 2, 3])
print 'Added as {0}'.format(resp['id'])
```

## Authentication

### HTTP Basic Authentication

HTTP Basic Authentication is supported by setting a username and password. This authentication mode is selected by NOT setting the `realm`. Credentials are sent on every request, without the `401` and `WWW-Authenticate` handshake.

### Shibboleth ECP

Shibboleth ECP is supported by setting a username and password, and setting the `realm` parameter to your IdP's ECP endpoint URL, e.g. `https://idp.grnoc.iu.edu/idp/profile/SAML2/SOAP/ECP`. If the SP asks for ECP authentication, a login request is launched to your IdP and, if successful, is sent to the SP. The original request is then re-sent with your login session cookie. Re-authentication is handled transparently (with additional latency if the login is required due to bouncing through the IdP).

Only username/password-based authentication is supported.

## Reserved method names

Any method not defined by the library is assumed to be a WS method. The following names are currently reserved by the library:

- Any name starting with a `_` is reserved for internal methods, or by Python.
- `ns` gets/sets the path to the GlobalNOC Service Discovery catalog file.
- `url` gets/sets the request URL.
- `urn` gets/sets the request URN. `ns` must be set before this is set. The lookup happens when this is set.
- `username` gets/sets the authentication username.
- `password` gets/sets the authentication password.
- `realm` gets/sets the authentication realm for ECP. Set to `None` to change from ECP to Basic.
- `raw` gets/sets whether the raw response is returned from remote method calls. If `False`, responses other content-type not matching `*/json`, or invalid JSON will raise a `RemoteMethodException`.
- `strict_content_type` get/sets whether non-`raw` mode requires `*/json` content type. Default `True`
- `session` gets/sets the underlying `requests.Session` object. Useful for making incompatible requests while benefiting from this library's ECP login help. If doing that, login still only happens during built-in WS calls, not calls directly on the `Session` object.
- `timeout` gets/sets the per-request timeout (in seconds).
- `_save` and `_load` save and load the current cookies in a `LWP` cookie jar file. This also saves/loads session cookies (as most login cookies are session cookies) so requests from multiple invocations can benefit from one login session. There is no locking around these files.

## Using ECP login without WSC

The `globalnoc.wsc.ECP` module implements the [requests](http://docs.python-requests.org/en/master/) custom authentication API. You can use that to perform ECP login without using the WSC calling convention. See the `requests` module documentation for how to use this.

**Note**: You'll want to use a `requests.Session` or you will log in on *every* request, not just once per end host per login lifetime. Logging in on every request increases request time, and increases load on the IdP.

```python
import requests
import globalnoc.wsc

username = '...'
password = '...'
realm = 'https://...'
url = 'https://...'

s = requests.Session()
c = s.get(url, auth=globalnoc.wsc.ECP(username, password, realm))
```
