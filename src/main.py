from .qmail import QmailFileManager
import yaml
from os.path import expandvars
from .officers import Officers
import logging
import sys
from box import Box

logging.basicConfig(stream=sys.stdout)


def main():
    # TODO: load from multiple places?
    try:
        with open('./config.yml', 'r') as conf:
            config = yaml.load(expandvars(conf.read()))
    except e:
        print('Do you have a config.yml?')
        exit()

    config = Box(config)
    fetcher = Officers(config)
    officers = fetcher.fetchOfficers()
    mapping = QmailFileManager.gennerateMapping(config, officers)
    manager = QmailFileManager(mapping=mapping)

    manager.printTable()
    manager.writeFS(outdir=config.config.outdir)

if __name__ == "__main__":
    main()
