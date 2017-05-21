import os
import xmlrpc.client
import time
import json

from concurrent.futures import ThreadPoolExecutor


def dump_package(package):
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

client = xmlrpc.client.ServerProxy('https://pypi.python.org/pypi')

packages = client.list_packages()

pool = ThreadPoolExecutor()

for package in packages:
    pool.submit(dump_package, package)


pool.shutdown()
