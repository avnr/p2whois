p2whois - Proxy to Prefix WhoIs
===

The `p2whois` package lets browser-based clients query ip addresses on [Prefix WhoIs][pwhois], a.k.a. pwhois. [Prefix
WhoIs][pwhois] collects ip routing information that can be usefull in applications, however, its interface uses
the whois protocol which is not available in browsers. So here is `p2whois`, a WSGI application that serves
as a proxy between the web client and the pwhois whois server. `p2whois` accepts a query via an HTTP GET request,
queries a pwhois server, and returns the pwhoise response formatted in a JSON-RPC style.

Please note that I'm not affiliated with Prefix WhoIs, I'm just a happy user of their service. To use
`p2whois` you must comply with the license terms of Prefix WhoIs, which can be found in their [web site][pwhois].

By default `pwhois` queries the whois server whose address is whois.pwhois.org, which is supposed to be routed
to the nearest pwhois mirror. You can change the whois server by modifying the default value of PWHOIS_SERVER,
for example, to your own pwhois mirror (see [pwhois] for instructions on setting up a mirror), using the
`conf` function (described below).

A demo p2whois server is currently deployed at <https://p2whois-avnr.rhcloud.com>. This server is not
configured for production purposes and its CORS policy will prevent queries from most domains, but you can play
with it in your browser. In addition, the `p2whois` package contains an `example` directory with a demo web
page that queries the p2whois demo server. You can view this demo page
[online](http://htmlpreview.github.io/?https://raw.github.com/avnr/p2whois/master/example/index.html).

The `p2whois` server expects two types of queries:

- **An empty query** such as `https://my-p2whois-server.com` will infer the caller's ip address from the HTTP
headers and will provide the pwhois data for that address.

- **A path in the format of an ip address** such as `https://my-p2whois-server.com/123.123.123.123` will query
the pwhois data for the requested address.

The result of the query is returned in a JSON-RPC-like format, i.e., as the object of a "result" member in a
JSON object. For example, <https://p2whois-avnr.rhcloud.com/4.4.4.4> returns (after formatting for
readability):

    {
        "result": {
            "City": "Broomfield",
            "Longitude": "-105.106477",
            "IP": "4.4.4.4",
            "Region": "Colorado",
            "Country": "United States",
            "Latitude": "39.882822",
            "Prefix": "4.0.0.0/9",
            "Country-Code": "US",
            "AS-Path": "3277 39710 9002 3356",
            "Origin-AS": "3356",
            "Net-Name": "LVLT-STATIC-4-4-16",
            "AS-Org-Name": "Level 3 Communications, Inc.",
            "Cache-Date": "1449492477",
            "Org-Name": "Level 3 Communications, Inc."
        }
    }

If an error occurs, the error code will be returned as both an HTTP status code and as a JSON-RPC error in
the response body as a member of an "error" member. Possible error codes are:

403 ACCESS FORBIDDEN - request cannot be served due to CORS restrictions, see more below.

404 NOT FOUND - a request was made for a misformed address, or the address is reserved (e.g., 127.0.0.1).


CORS
---

In order to prevent leeching of your servers running p2whois, and possibly overloading under your identity
the Prefix WhoIs servers (or your pwhois servers if you run a mirror), the `p2whois` application implements a CORS
policy. The policy is set in the value of `ORIGINS`. By default `ORIGINS = []`, meaning that any domain
can query the `p2whois` server. If you set `ORIGINS` to a list of origins (i.e., hosts and ports), only those
listed origins will be served by the application. For example, `ORIGINS = [ 'http://mysite.com' ]` will only serve
requests that originate from `http://mysite.com` and will reject all other requests with a 403 HTTP status.

Note that CORS does not secure the application and does not prevent servers from querying it, only browsers.

Test Server
---

`p2whois` has a built in test server that enables you to run it directly from the command line. You can run it
directly:

    $ python p2whois.py

or, if it is on the modules path (e.g., if it was installed by `pip`):

    $ python -m p2whois

The test server listens by default on a port 8043, and can then be reached from a browser at 
`http://localhost:8043`.

Installation and Use
---

You have several options for installing `p2whois`:

- Copy the file `p2whois.py` to your project. It is just a single file with no dependencies. Or,

- Install using `pip install p2whois`. Or,

- Clone the project from GitHub - `git clone https://github.com/avnr/p2whois`.

Requires Python3. Import with `import p2whois`, and call `p2whois.application` from your preferred WSGI server.

To change the default settings use the `conf` function:

    import p2whois
    
    p2whois.conf(
        origins = [
            'http://mywebhost.com', 'http://www.mywebhost.com',
            'https://mywebhost.com', 'https://www.mywebhost.com' ],
        pwhois_server = 'pwhois.mymirror.net',
        pwhois_port = 4300 )
    
    ...
    srv = make_server( '0.0.0.0', 80, p2whois.application )
        
All arguments of the `conf` function are optional. THIS FUNCTION IS NOT THREAD-SAFE, CALL IT BEFORE FIRING
THE FIRST THREAD.

License
---

MIT License

The returned data is subject to the [pwhois license][pwhois].


[pwhois]: http://pwhois.org