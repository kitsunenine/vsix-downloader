#!/usr/bin/python
import sys,os,argparse
import re, json
import requests
URL=sys.argv[1]

if '=' not in URL:
    raise ValueError("URL needs to have an itemname in it.")
itemname=URL.split('=')[1]
user=itemname.split('.')[0]
module=itemname.split('.')[1]

page = requests.get(URL).text
script=re.search('<script[^>]*class="vss-extension"[^>]*>(.*)</script>',page)
if not script:
   raise ValueError("I can't find any versions.")
j = json.loads(script.group(1))
versions = [q['version'] for q in j['versions']]
version = max(versions)

vsix_url='http://'+user+'.gallery.vsassets.io/_apis/public/gallery/publisher/'+user+'/extension/'+module+'/'+version+'/assetbyname/Microsoft.VisualStudio.Services.VSIXPackage'
filename = '.'.join([user,module,version,'vsix'])
print('Writing to '+filename+' ...')
with open(filename,'w') as f:
    f.write(requests.get(vsix_url).content)
