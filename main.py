import os
import requests
from box import Box
import datetime


class QmailFileManager(object):
    def __init__(self, path=None, mapping={}):
        self._path = path;
        if path is None:
            self._files = mapping
        else:
            self._files = self.loadInternalRepresentation(path)


    @staticmethod
    def loadInternalRepresentation(path):
        aliasdict = {}
        emails = map(lambda x: x[7:], filter(lambda x: x.startswith('.qmail-'), os.listdir(path)))
        for alias in emails:
            with open(path + '/.qmail-' + alias) as mapfile:
                aliasdict[alias] = list(map(lambda a: a.strip()[1:], mapfile.readlines()))
        return aliasdict


    def printTable(self):
        print('Alias')
        for key in self._files:
            print(key + ": " + str(", ".join(self._files[key])))


    def writeFS(self, override=None):
        path_dir = None
        if self._path is not None:
            path_dir = self._path
        if override is not None:
            path_dir = override
        if path_dir is None:
            raise "No output path"

        for key in self._files:
            with open(path_dir + '/.qmail-' + key, 'w') as alias:
                for out in self._files[key]:
                    alias.write('&' + out + '\n')


def fetchOfficers(page=1):
    params = {
        'active': datetime.date.today(),
        'page': page
    }
    resp = requests.get('https://sse.rit.edu/api/v2/officers', params=params)
    data = Box(resp.json())

    if data.total > page * data.perPage:
        return data.data.to_list() + fetchOfficers(page + 1)
    else:
        return data.data.to_list()


def main():

    officers = fetchOfficers()

    mapping = {}

    for officer in officers:
        officer = Box(officer)
        mapto = mapping.get(officer.email, [])
        mapto.append(officer.userDce + '@rit.edu')
        mapping[officer.email] = mapto

    manager = QmailFileManager(mapping=mapping)
    manager.printTable()
    manager.writeFS(override='/qmail')


if __name__ == "__main__":
    main()
