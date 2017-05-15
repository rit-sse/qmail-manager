import os
import logging
from box import Box

logger = logging.getLogger('qmail')
logger.setLevel(logging.INFO)


class QmailFileManager(object):
    def __init__(self, path=None, mapping={}):
        self._path = path
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
        for key in self._files:
            logger.info(key + ": " + str(", ".join(self._files[key])))

    def writeFS(self, outdir=None):
        """
        Write the qmail filesystem, note does not delete any unused alias.
        TODO: remove unused aliases
        """
        path_dir = None
        if self._path is not None:
            path_dir = self._path
        if outdir is not None:
            path_dir = outdir
        if path_dir is None:
            raise "No output path"

        for key in self._files:
            with open(path_dir + '/.qmail-' + key, 'w') as alias:
                for out in self._files[key]:
                    alias.write('&' + out + '\n')

    @staticmethod
    def gennerateMapping(config, officers):
        mapping = {}
        # map joining emails
        for default_map in config.defaults.join_emails:
            for mapfrom in config.defaults.join_emails[default_map]:
                mapto = mapping.get(mapfrom, [])
                mapto.append(default_map + '@sse.rit.edu')
                mapping[mapfrom] = mapto

        # map mailing lists
        for spread in config.defaults.spread_emails:
            mapto = mapping.get(spread, [])
            mapto = mapto + list(map(lambda e: e + '@sse.rit.edu', config.defaults.spread_emails[spread]))
            mapping[spread] = mapto

        # add all the officers from the app
        for officer in officers:
            officer = Box(officer)
            mapto = mapping.get(officer.email, [])
            mapto.append(officer.userDce + '@rit.edu')
            mapping[officer.email] = mapto

        return mapping
