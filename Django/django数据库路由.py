"""
django ORM数据模型配置数据库

django支持多个数据库，通过djangoORM定义数据模型，比如class User(Model), 无法通过class Meta
配置管理该数据模型对应的数据库，只能使用默认数据defautl.

django ConnectionRouter 解决数据模型与数据库映射
"""


# 实现DB router
import logging
from django.conf import settings

_logger = logging.getLogger('django')


class DatabaseRouter(object):
    """
    Database router to control the  models for differrent db.
    """

    DEFAULT_DB = 'default'

    def _db(self, model, **hints):
        # 给model添加属性 _database, 然后根据model定义的该属性，来判断应该读取哪一个数据库
        db = getattr(model, '_database', None)
        if not db:
            return self.DEFAULT_DB

        if db in settings.DATABASES.keys():
            return db
        else:
            _logger.warn('%s not exist' % db)
            return self.DEFAULT_DB

    def db_for_read(self, model, **hints):
        return self._db(model, **hints)

    def db_for_write(self, model, **hints):
        return self._db(model, **hints)


# 配置DB routers

DATABASE_ROUTERS = ['db_router.DatabaseRouter']


# 为Model制定数据库


class User(Model):
    _database = 'user_db'

    class Meta:
        db_table = 'user'

    ...

"""
django通过ConnectionRouter管理数据库路由
django/db/utils.py
"""


class ConnectionRouter(object):

    def __init__(self, routers=None):
        """
        If routers is not specified, default to settings.DATABASE_ROUTERS.
        """
        self._routers = routers

    @cached_property
    def routers(self):
        if self._routers is None:
            self._routers = settings.DATABASE_ROUTERS
        routers = []
        for r in self._routers:
            if isinstance(r, six.string_types):
                router = import_string(r)()
            else:
                router = r
            routers.append(router)
        return routers

    def _router_func(action):
        def _route_db(self, model, **hints):
            chosen_db = None
            for router in self.routers:
                try:
                    method = getattr(router, action)
                except AttributeError:
                    # If the router doesn't have a method, skip to the next one.
                    pass
                else:
                    chosen_db = method(model, **hints)
                    if chosen_db:
                        return chosen_db
            instance = hints.get('instance')
            if instance is not None and instance._state.db:
                return instance._state.db
            return DEFAULT_DB_ALIAS

        return _route_db

    db_for_read = _router_func('db_for_read')
    db_for_write = _router_func('db_for_write')

