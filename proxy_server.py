#!/usr/bin/env python2

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import argparse
import os
import random
import sys
import requests
import re
from urllib import unquote
import json

hostname = '127.0.0.1'

def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z

def set_header():
    headers = {
        'Host': hostname
    }

    return headers

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.0'
    def do_HEAD(self):
        self.do_GET(body=False)

    def do_GET(self, body=True):
        sent = False
        safe = True
        try:
            url = 'http://{}{}'.format(hostname, self.path)
            req_header = self.parse_headers()
            if '/rce.php' in self.path:
                safe = check_RCE(url)
            if not safe:
                url = 'http://{}{}'.format(hostname, '/forbidden')
            print req_header
            log(json.dumps(req_header))
            print url
            log(url)
            
            resp = requests.get(url, headers=merge_two_dicts(req_header, set_header()), verify=False)
            sent = True
            
            self.send_response(resp.status_code)
            self.send_resp_headers(resp)
            if body:
                self.wfile.write(resp.content)
            return
        finally:
            self.finish()
            if not sent:
                self.send_error(404, 'error trying to proxy')

    def do_POST(self, body=True):
        sent = False
        safe = True
        try:
            url = 'http://{}{}'.format(hostname, self.path)
            content_len = int(self.headers.getheader('content-length', 0))
            post_body = self.rfile.read(content_len)
            req_header = self.parse_headers()
            
            if '/rce.php' in self.path:
                safe = check_RCE(url)
            if not safe:
                url = 'http://{}{}'.format(hostname, '/forbidden')
            print req_header
            print url
            			
            resp = requests.post(url, data=post_body, headers=merge_two_dicts(req_header, set_header()), verify=False)
            sent = True

            self.send_response(resp.status_code)
            self.send_resp_headers(resp)
            if body:
                self.wfile.write(resp.content)
            return
        finally:
            self.finish()
            if not sent:
                self.send_error(404, 'error trying to proxy')

    def parse_headers(self):
        req_header = {}
        for line in self.headers.headers:
            line_parts = [o.strip() for o in line.split(':', 1)]
            if len(line_parts) == 2:
                req_header[line_parts[0]] = line_parts[1]
        return req_header

    def send_resp_headers(self, resp):
        respheaders = resp.headers
        print 'Response Header'
        for key in respheaders:
            if key not in ['Content-Encoding', 'Transfer-Encoding', 'content-encoding', 'transfer-encoding', 'content-length', 'Content-Length']:
	            print key,": ", respheaders[key]
	            log(key + ": " + respheaders[key])
	            self.send_header(key, respheaders[key])
        print 'Content-Length: ', len(resp.content)
        log('Content-Length: ' + str(len(resp.content)))
        self.send_header('Content-Length', len(resp.content))
        self.end_headers()

def check_RCE(url):
    try:
        url = unquote(url).decode('utf8')
    except AttributeError:
        print("URL does not contain encoded strings")

    if '?ip' in url:
        data = url.split('=')[1]
    else:
        data = ''

    if re.search('(?i);|\{|\||\&|\\n|\\r|\$\(.*[\)]*|`|\$\{|<\(.*[\)]*|>\(.*[\)]*|\(\s*\)|\?|\\[\d]+', data.lower()):
        print 'Remote Command Execution: Unix Command Injection'
        print 'Matched: ' + data
        return False
    
    commands_regex = open('commands_regex.txt', 'r').read()
    if re.search(commands_regex, data.lower()):
        print 'Remote Command Execution: Unix Command Injection'
        print 'Matched Unix command: ' + data
        return False
    
    return True
			 
def log(data):
    with open('access.log', 'a') as log_file:
        log_file.write(data + '\n')

def parse_args(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(description='Proxy HTTP requests')
    parser.add_argument('--port', dest='port', type=int, default=8080,
                        help='serve HTTP requests on specified port (default: random)')
    args = parser.parse_args(argv)
    return args

def main(argv=sys.argv[1:]):
    args = parse_args(argv)
    print('http server is starting on port {}...'.format(args.port))
    server_address = ('127.0.0.1', args.port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print('http server is running as reverse proxy')
    httpd.serve_forever()

if __name__ == '__main__':
    main()
    