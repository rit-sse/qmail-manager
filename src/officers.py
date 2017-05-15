import logging
from urllib.parse import urlparse
import requests
from box import Box
import datetime

logger = logging.getLogger('officers')
logger.setLevel(logging.INFO)


class Officers(object):
    def __init__(self, config):
        self._api_root = config['config']['api']
        try:
            urlparse(self._api_root)
        except e:
            raise "Invalid API_ROOT set"
        logger.info('API pointed to %s', self._api_root)

    def fetchOfficers(self, page=1):
        """
        recursively fetch all officers currently active
        """
        params = {
            'active': datetime.date.today(),
            'page': page
        }
        resp = requests.get(self._api_root + '/officers', params=params)
        data = Box(resp.json())

        if data.total > page * data.perPage:
            return data.data.to_list() + self.fetchOfficers(page + 1)
        else:
            return data.data.to_list()
