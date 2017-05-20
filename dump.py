import os
import xmlrpc.client
import json

client = xmlrpc.client.ServerProxy('https://pypi.python.org/pypi')

packages = client.list_packages()

for package in packages:
    filepath = '%s.json' % package
    if os.path.exists(filepath):
        print('skipping ', package)
        continue

    versions = [client.release_data(package, version) for version in client.package_releases(package, True)]

    with open(filepath, 'w') as f:
        for v in versions:
            f.write(json.dumps(v) + '\n')


    print('Done ', package)

