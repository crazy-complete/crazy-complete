# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completes HTTP methods, status codes, and header field names.'''

from .. import messages as m
from ..errors import CrazySchemaValidationError
from ..scheme_validator import check_non_empty_string, check_type

CATEGORY = 'basic'

SYNOPSIS = r'''
['http', <TYPE>]
'''

SHORT = 'Complete HTTP methods, status codes, and header field names'

LONG = r'''
`TYPE`:
  One of the following values:

    - `method`: HTTP methods
    - `code`: HTTP status codes
    - `header`: all standard HTTP header field names
    - `request_header`: header field names the client sends in a request
    - `response_header`: header field names the server sends in a response
'''

ALSO = {
    'choices': 'For completing from a custom set of values',
}

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--method']
    complete: ['http', 'method']

  - option_strings: ['--status']
    complete: ['http', 'code']

  - option_strings: ['--header']
    complete: ['http', 'header']

  - option_strings: ['--request-header']
    complete: ['http', 'request_header']

  - option_strings: ['--response-header']
    complete: ['http', 'response_header']
'''

OUTPUT = r'''
~ > example --method=<TAB>
ACL              OPTIONS
BASELINE-CONTROL ORDERPATCH
BIND             PATCH
CHECKIN          POST
CHECKOUT         PRI
CONNECT          PROPFIND
COPY             PROPPATCH
[...]

~ > example --status=<TAB>
200  (OK)                   302  (Found)
201  (Created)              304  (Not Modified)
204  (No Content)           404  (Not Found)
301  (Moved Permanently)    500  (Internal Server Error)
[...]

~ > example --request-header=<TAB>
Accept          (Media-type preferences for the response)
Host            (Target host of the request (required, HTTP/1.1))
Range           (Request a byte range of the representation)
User-Agent      (Client application, OS and browser info)
If-None-Match   (Apply only if no entity tag matches)
Content-Length  (Size of the payload in octets)
[...]

~ > example --response-header=<TAB>
Cache-Control  (Caching directives (no-cache, no-store, max-age, ...))
Content-Type   (Media type of the payload)
ETag           (Opaque validator for the response version)
Location       (Target URI of a redirect response)
Vary           (Request fields that must key cached responses)
Set-Cookie     (Set an HTTP cookie on the client (RFC 6265))
[...]
'''

_error = CrazySchemaValidationError


_METHODS = [
    'ACL',
    'BASELINE-CONTROL',
    'BIND',
    'CHECKIN',
    'CHECKOUT',
    'CONNECT',
    'COPY',
    'DELETE',
    'GET',
    'HEAD',
    'LABEL',
    'LINK',
    'LOCK',
    'MERGE',
    'MKACTIVITY',
    'MKCALENDAR',
    'MKCOL',
    'MKREDIRECTREF',
    'MKWORKSPACE',
    'MOVE',
    'OPTIONS',
    'ORDERPATCH',
    'PATCH',
    'POST',
    'PRI',
    'PROPFIND',
    'PROPPATCH',
    'PUT',
    'QUERY',
    'REBIND',
    'REPORT',
    'SEARCH',
    'TRACE',
    'UNBIND',
    'UNCHECKOUT',
    'UNLINK',
    'UNLOCK',
    'UPDATE',
    'UPDATEREDIRECTREF',
    'VERSION-CONTROL',
]


_CODES = [
    ('100', 'Continue'),
    ('101', 'Switching Protocols'),
    ('102', 'Processing'),
    ('103', 'Early Hints'),
    ('104', 'Upload Resumption Supported (TEMPORARY - registered 2024-11-13, extension registered 2025-09-15, expires 2026-11-13)'),
    ('200', 'OK'),
    ('201', 'Created'),
    ('202', 'Accepted'),
    ('203', 'Non-Authoritative Information'),
    ('204', 'No Content'),
    ('205', 'Reset Content'),
    ('206', 'Partial Content'),
    ('207', 'Multi-Status'),
    ('208', 'Already Reported'),
    ('226', 'IM Used'),
    ('300', 'Multiple Choices'),
    ('301', 'Moved Permanently'),
    ('302', 'Found'),
    ('303', 'See Other'),
    ('304', 'Not Modified'),
    ('305', 'Use Proxy'),
    ('307', 'Temporary Redirect'),
    ('308', 'Permanent Redirect'),
    ('400', 'Bad Request'),
    ('401', 'Unauthorized'),
    ('402', 'Payment Required'),
    ('403', 'Forbidden'),
    ('404', 'Not Found'),
    ('405', 'Method Not Allowed'),
    ('406', 'Not Acceptable'),
    ('407', 'Proxy Authentication Required'),
    ('408', 'Request Timeout'),
    ('409', 'Conflict'),
    ('410', 'Gone'),
    ('411', 'Length Required'),
    ('412', 'Precondition Failed'),
    ('413', 'Content Too Large'),
    ('414', 'URI Too Long'),
    ('415', 'Unsupported Media Type'),
    ('416', 'Range Not Satisfiable'),
    ('417', 'Expectation Failed'),
    ('421', 'Misdirected Request'),
    ('422', 'Unprocessable Content'),
    ('423', 'Locked'),
    ('424', 'Failed Dependency'),
    ('425', 'Too Early'),
    ('426', 'Upgrade Required'),
    ('428', 'Precondition Required'),
    ('429', 'Too Many Requests'),
    ('431', 'Request Header Fields Too Large'),
    ('451', 'Unavailable For Legal Reasons'),
    ('500', 'Internal Server Error'),
    ('501', 'Not Implemented'),
    ('502', 'Bad Gateway'),
    ('503', 'Service Unavailable'),
    ('504', 'Gateway Timeout'),
    ('505', 'HTTP Version Not Supported'),
    ('506', 'Variant Also Negotiates'),
    ('507', 'Insufficient Storage'),
    ('508', 'Loop Detected'),
    ('510', 'Not Extended (OBSOLETED)'),
    ('511', 'Network Authentication Required'),
]


_REQUEST_HEADERS = [
    ('Access-Control-Request-Headers', 'CORS preflight: request fields the client intends to send'),
    ('Access-Control-Request-Method', 'CORS preflight: HTTP method of the actual request'),
    ('Accept', 'Media-type preferences for the response'),
    ('Accept-Charset', 'Preferred character encodings'),
    ('Accept-Encoding', 'Preferred content codings (gzip, br, ...)'),
    ('Accept-Language', 'Preferred natural languages'),
    ('Authorization', 'Credentials to authenticate with the origin server'),
    ('Cookie', 'HTTP cookies on the client (RFC 6265)'),
    ('Expect', 'Behaviors expected of the recipient (e.g. 100-continue)'),
    ('Forwarded', 'Original client information relayed through proxies'),
    ('From', 'Email address of the sender'),
    ('Host', 'Target host of the request (required, HTTP/1.1)'),
    ('If-Match', 'Apply only if the entity tags match'),
    ('If-Modified-Since', 'Apply only if the resource is newer than the given date'),
    ('If-None-Match', 'Apply only if no entity tag matches'),
    ('If-Range', 'Apply Range only if the given precondition holds'),
    ('If-Unmodified-Since', 'Apply only if the resource is older than the given date'),
    ('Max-Forwards', 'Remaining hop limit for TRACE'),
    ('Origin', 'CORS: origin of the request'),
    ('Proxy-Authorization', 'Credentials to authenticate with a proxy'),
    ('Purposed', 'Experimental: the purpose of the request'),
    ('Range', 'Request a byte range of the representation'),
    ('Referer', 'Address of the referring document'),
    ('Sec-CH-UA', 'Client hint: user-agent brand/version'),
    ('Sec-Fetch-Dest', 'Client hint: destination category'),
    ('Sec-Fetch-Mode', 'Client hint: fetch mode'),
    ('Sec-Fetch-Site', 'Client hint: origin relationship'),
    ('Sec-Fetch-User', 'Client hint: user activation present'),
    ('TE', 'Transfer codings acceptable to the client'),
    ('User-Agent', 'Client application, OS and browser info'),
    ('Cache-Control', 'Caching directives (no-cache, no-store, max-age, ...)'),
    ('Connection', 'Per-connection options (keep-alive, close, upgrade)'),
    ('Content-Encoding', 'Coding applied to the representation (gzip, br)'),
    ('Content-Language', 'Natural language of the audience'),
    ('Content-Length', 'Size of the payload in octets'),
    ('Content-Type', 'Media type of the payload'),
    ('Date', 'Date and time the message was generated'),
    ('Trailer', 'Additional field names sent in a chunked-message trailer'),
    ('Transfer-Encoding', 'Coding applied for transport (chunked)'),
    ('Upgrade', 'Request/response to switch connection protocols'),
    ('Via', 'Proxies/gateways the message passed through'),
]


_RESPONSE_HEADERS = [
    ('Cache-Control', 'Caching directives (no-cache, no-store, max-age, ...)'),
    ('Connection', 'Per-connection options (keep-alive, close, upgrade)'),
    ('Content-Encoding', 'Coding applied to the representation (gzip, br)'),
    ('Content-Language', 'Natural language of the audience'),
    ('Content-Length', 'Size of the payload in octets'),
    ('Content-Type', 'Media type of the payload'),
    ('Date', 'Date and time the message was generated'),
    ('Trailer', 'Additional field names sent in a chunked-message trailer'),
    ('Transfer-Encoding', 'Coding applied for transport (chunked)'),
    ('Upgrade', 'Request/response to switch connection protocols'),
    ('Via', 'Proxies/gateways the message passed through'),
    ('Accept-Ranges', 'Range units supported (e.g. "bytes")'),
    ('Access-Control-Allow-Credentials', 'CORS: credentials may be included in the request'),
    ('Access-Control-Allow-Headers', 'CORS: request fields allowed in the actual request'),
    ('Access-Control-Allow-Methods', 'CORS: HTTP methods allowed in the actual request'),
    ('Access-Control-Allow-Origin', 'CORS: origins allowed to read the resource'),
    ('Access-Control-Expose-Headers', 'CORS: response fields the client may read'),
    ('Access-Control-Max-Age', 'CORS: how long to cache a preflight response'),
    ('Age', 'Seconds the response has been held in a cache'),
    ('Alt-Svc', 'Alternative protocols/endpoints for the host'),
    ('Content-Disposition', 'Intended presentation (inline; filename=...)'),
    ('Content-Location', 'Alternate location of the returned data'),
    ('Content-Range', 'Byte range of this response within the full representation'),
    ('ETag', 'Opaque validator for the response version'),
    ('Last-Modified', 'Last modification time of the resource'),
    ('Link', 'Hyperlinks to related resources (RFC 5988)'),
    ('Location', 'Target URI of a redirect response'),
    ('NEL', 'Network Error Reporting configuration'),
    ('Proxy-Authenticate', 'Challenge the client to authenticate through a proxy'),
    ('Proxy-Status', 'Status information supplied by a proxy'),
    ('Retry-After', 'When the client should retry (429/503)'),
    ('Server', 'Server software identification'),
    ('Set-Cookie', 'Set an HTTP cookie on the client (RFC 6265)'),
    ('Timing-Allow-Origin', 'Origins allowed to read performance resource timing'),
    ('Vary', 'Request fields that must key cached responses'),
    ('Warning', 'Non-standard caveats about the payload'),
    ('WWW-Authenticate', 'Challenge the client to authenticate'),
]


_HEADERS = list({**dict(_REQUEST_HEADERS), **dict(_RESPONSE_HEADERS)}.items())


_DATA = {
    'method': _METHODS,
    'code': dict(_CODES),
    'header': dict(_HEADERS),
    'request_header': dict(_REQUEST_HEADERS),
    'response_header': dict(_RESPONSE_HEADERS),
}


def validate(_ctxt, arguments):
    '''Validate YAML for the http completer'''
    type_ = arguments.get_required_arg('type')
    arguments.require_no_more()

    check_type(type_, (str,), 'type')
    check_non_empty_string(type_, 'type')

    if type_.value not in _DATA:
        values = ', '.join('`%s`' % key for key in _DATA)
        message = '%s: %s' % (type_, m.invalid_value_expected_values(values))
        raise _error(message, type_)


def bash(completer, ctxt, trace, type_):
    '''Implement http for bash'''
    return completer.complete_from_def(ctxt, trace, ['choices', _DATA[type_]])


def fish(completer, ctxt, trace, type_):
    '''Implement http for fish'''
    return completer.complete_from_def(ctxt, trace, ['choices', _DATA[type_]])


def zsh(completer, ctxt, trace, type_):
    '''Implement http for zsh'''
    return completer.complete_from_def(ctxt, trace, ['choices', _DATA[type_]])
