import os
import xmlrpc.client
import time
import json
import lxml.html
import threading

from urllib.request import urlopen
from concurrent.futures import ThreadPoolExecutor


def dump_package(package):
    tls = threading.local()
    # Reuse the ServerProxy objects!
    if hasattr(tls, 'client'):
        client = tls.client
    else:
        client = xmlrpc.client.ServerProxy('https://pypi.python.org/pypi')
        tls.client = client
    filepath = '%s.json' % package
    if os.path.exists(filepath):
        print('skipping ', package)
        return

    start_time = time.time()
    versions = [client.release_data(package, version) for version in client.package_releases(package, True)]

    with open(filepath, 'w') as f:
        for v in versions:
            f.write(json.dumps(v) + '\n')


    print('Done {} in {}s'.format(package, time.time() - start_time))


simple_doc = lxml.html.parse(urlopen('https://pypi.python.org/simple/'))
pool = ThreadPoolExecutor()

for _, _, package, _ in simple_doc.getroot().iterlinks():
    pool.submit(dump_package, package)


pool.shutdown()
