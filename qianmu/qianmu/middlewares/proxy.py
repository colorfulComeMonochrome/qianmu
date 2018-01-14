import random
import logging
from scrapy.exceptions import NotConfigured
from urllib.request import _parse_proxy

logger = logging.getLogger(__name__)


# 解析代理服务器的ip
def _parse(proxy_url):
    proxy_type, user, password, hostport = _parse_proxy(proxy_url)
    return '%s://%s' % (proxy_type, hostport)


class RandomProxyMiddleware(object):
    def __init__(self, settings):
        self.proxies = settings.getlist('PROXIES')
        self.max_failed_times = settings.getint('FAILED_REQUEST_NUM', 1)
        self.stats = {}.fromkeys(map(_parse, self.proxies), 0)

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('HTTPPROXY_ENABLED'):
            raise NotConfigured
        if not crawler.settings.getlist('PROXIES'):
            raise NotConfigured
        return cls(crawler.settings)

    def process_request(self, request, spider):
        request.meta['proxy'] = random.choice(self.proxies)

    def process_response(self, request, response, spider):
        # 获取当次请求所用的代理ip
        cur_proxy = request.meta['proxy']
        logger.info(cur_proxy)
        if response.status >= 400:
            self.stats[cur_proxy] += 1
            logger.info('%s proxy request has failed' % cur_proxy)
        if self.stats[cur_proxy] >= self.max_failed_times:
            for proxy in self.proxies:
                *_, hostport = _parse_proxy(proxy)
                if cur_proxy.endswith(hostport):
                    self.proxies.remove(cur_proxy)
                    logger.warning('%s proxy has beyond max_failed_times,removed' % cur_proxy)
                    break
        return response
