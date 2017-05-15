import os

class QmailFileManager(object):
    def __init__(self):
        self._files = self.loadInternalRepresentation('/qmail')


    @staticmethod
    def loadInternalRepresentation(path):
        aliasdict = {}
        emails = map(lambda x: x[7:], os.listdir(path))
        for alias in emails:
            with open(path + '/.qmail-' + alias) as mapfile:
                aliasdict[alias] = list(map(lambda a: a.strip()[1:], mapfile.readlines()))
        return aliasdict

def main():
    manager = QmailFileManager()
    print(manager._files)

if __name__ == "__main__":
    main()
