import faker
from lazyspider import lazyheaders

class RandomUseragentMiddleware(object):
    def __init__(self, settings):
        self.faker = faker.Faker()

    # classmethod装饰器表示
    # 对于定义了classmethod的方法,cls表示这个类本身
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        # request.headers['User-Agent'] = self.faker.user_agent()
        request.headers['User-Agent'] = 'shuoshuoshuoshuoshuoshuoshuoshuoshuoshuoshuoshuoshuo'
