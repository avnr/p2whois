#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#    p2whois version 0.5 - Proxy to Prefix WhoIs
#    Copyright (c) 2015 Avner Herskovits
#
#    For documentation please refer to the accompanying README.md file.
#
#    The license below covers this package only. To access and use data obtained
#    from  Prefix WhoIs you must comply with the relevant Prefix WhoIs licenses,
#    please consult http://pwhois.org.
#
#    p2whois is not affiliated with Prefix WhoIs.
#
#    MIT License
#
#    Permission  is  hereby granted, free of charge, to any person  obtaining  a
#    copy of this  software and associated documentation files (the "Software"),
#    to deal in the Software  without  restriction, including without limitation
#    the rights to use, copy, modify, merge,  publish,  distribute,  sublicense,
#    and/or  sell  copies of  the  Software,  and to permit persons to whom  the
#    Software is furnished to do so, subject to the following conditions:
#
#    The above copyright notice and this  permission notice shall be included in
#    all copies or substantial portions of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT  WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE  WARRANTIES  OF  MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR  ANY  CLAIM,  DAMAGES  OR  OTHER
#    LIABILITY, WHETHER IN AN  ACTION  OF  CONTRACT,  TORT OR OTHERWISE, ARISING
#    FROM,  OUT  OF  OR  IN  CONNECTION WITH THE SOFTWARE OR THE  USE  OR  OTHER
#    DEALINGS IN THE SOFTWARE.
#

#
# Imports - stdlib only
#
from json   import dumps
from socket import AF_INET, SOCK_STREAM, socket

#
# Configuration paramteres
#
ORIGINS = []                        # Empty = all origins allowed ( "*" ), add specific domains to limit CORS
PWHOIS_SERVER = 'whois.pwhois.org'  # Resolves to nearest pwhois mirror; to start your own mirror consult http://pwhois.org
PWHOIS_PORT = 43                    # Port for whois query

#
# Change default configuration
#
# THIS FUNCTION IS NOT THREAD-SAFE, CALL BEFORE FIRING THE FIRST THREAD
#
def conf( origins = ORIGINS, pwhois_server = PWHOIS_SERVER, pwhois_port = PWHOIS_PORT ):
    global ORIGINS
    global PWHOIS_SERVER
    global PWHOIS_PORT
    ORIGINS = origins
    PWHOIS_SERVER = pwhois_server
    PWHOIS_PORT = pwhois_port

#
# A simple whois client
#
def _whois( ip ):
    s = socket( AF_INET, SOCK_STREAM )
    s. connect(( PWHOIS_SERVER, PWHOIS_PORT ))
    s.send(( ip + '\r\n' ). encode( 'utf-8' ))
    res, i = b'', b'START'
    while len( i ):
        i = s. recv( 1024 )
        res += i
    return res. decode( 'utf-8' )

#
# The WSGI application
#
def application( env, respond ):
    origin = env. get( 'HTTP_ORIGIN' )
    headers = [( 'Access-Control-Allow-Methods', 'GET, OPTIONS' )]
    headers. append(( 'Access-Control-Max-Age', '1728000' ))
    headers. append(( 'Content-type', 'text/plain' ))
    if ORIGINS:
        if not origin or origin not in ORIGINS:
            respond( '403 ACCESS FORBIDDEN', [( 'Content-type', 'text/plain' )])
            return [ b'{"error":{"code":403,"message":"ACCESS FORBIDDEN"}}' ]
        else:
            headers. append(( 'Access-Control-Allow-Origin', origin ))
    else:
        headers. append(( 'Access-Control-Allow-Origin', '*' ))
    request_method = env. get( 'REQUEST_METHOD' ). casefold()
    if 'get' == request_method:
        path = env. get( 'PATH_INFO' )
        if '/' == path:
            ip = env. get( 'HTTP_X_FORWARDED_FOR' )
            if ip:
                ip = ip. split( ',' )[ -1 ]. strip()
            else:
                ip = env. get( 'REMOTE_ADDR' )
        else:
            ip = path[ 1: ]
        res = {}
        for i in _whois( ip ). split( '\n' ):
            j = i. split( ':', 1 )
            if 2 == len( j ) and ' ' not in j[ 0 ]:
                res[ j[ 0 ]] = j[ 1 ]. strip()
        if len( res ):
            respond( '200 OK', headers )
            return [ dumps({ 'result': res }, separators = ( ',', ':' )). encode( 'utf-8' )]
        else:
            respond( '404 NOT FOUND', headers )
            return [ b'{"error":{"code":404,"message":"NOT FOUND"}}' ]
    elif 'options' == request_method:
        respond( '200 OK', headers )
        return []
    else:
        respond( '400 BAD REQUEST', [( 'Content-type', 'text/plain' )])
        return []

#
# Test server
#
def main():
    from socketserver           import ThreadingMixIn
    from wsgiref. simple_server import make_server, WSGIServer

    PORT = 8043                         # Relevant for test server only

    class _Wsgi_t( ThreadingMixIn, WSGIServer ): pass

    print( 'Press CTRL-C to quit' )
    srv = make_server( '0.0.0.0', PORT, application, _Wsgi_t )
    try:
        srv. serve_forever()
    except KeyboardInterrupt: pass
    finally:
        srv. server_close()
    print( 'Bye.' )

if '__main__' == __name__:
    main()