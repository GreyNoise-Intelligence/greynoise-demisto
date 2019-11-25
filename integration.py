import requests

def mergedicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z

def sendRequest(method, url, uri, apikey, data = None):
    res = None
    headers = {'key': apikey}

    if method.lower() == 'get':
        #res = requests.get(url + uri, auth = (user, passwd))
        res = requests.get(url + uri, headers=headers, data=data)

    if res.status_code >= 400:
        if res.text.startswith('{'):
            return '### Error: ' + str(res.status_code) + ': ' + res.json()["error"]
        else:
            return '### Error: ' + str(res.status_code)

    return res.text

res = []
apikey = demisto.params()['apikey']
url = demisto.params()['url']
data = None

#What happens when the 'Test' button is pressed
if demisto.command() == 'test-module':
    res = sendRequest('get', url, "/v2/noise/quick/8.8.8.8", apikey)
    if res.startswith('### Error:'):
        demisto.results( { 'Type' : entryTypes['error'], 'ContentsFormat' : 'text', 'Contents' : res } )
    elif 'noise' in res:
        demisto.results('ok')
else:
    if "date" in demisto.args():
        date = demisto.args()['date']
    if "ip" in demisto.args():
        ip = demisto.args()['ip']
    if "ips" in demisto.args():
        iplist = demisto.args()['ips'].split(",")

    elif demisto.command() == 'greynoise-quickcheck':
        uri = '/v2/noise/quick/' + ip
        method = 'get'
    elif demisto.command() == 'greynoise-context':
        uri = '/v2/noise/context/' + ip
        method = 'get'
    elif demisto.command() == 'greynoise-actors':
        uri = '/v2/research/actors/'
        method = 'get'
    elif demisto.command() == 'greynoise-multicheck':
        uri = '/v2/noise/multi/quick'
        method = 'get'
        tmpdata = dict()
        tmpdata['ips'] = iplist
        data=json.dumps(tmpdata)

    res = sendRequest(method, url, uri, apikey, data)

    if res.startswith('### Error:'):
        demisto.results( { 'Type' : entryTypes['error'], 'ContentsFormat' : 'text', 'Contents' : res } )
        sys.exit(0)
    elif res.startswith('{'):
        res = json.loads(res)

    demisto.results(res)

sys.exit(0)
