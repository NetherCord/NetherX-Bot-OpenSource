import os
import pickle
import shutil

from operations.config import get_from_config

BASE_DIR = os.environ["NETHERX_BASE_DIR"]
caching_dir_path = os.path.join(BASE_DIR, *get_from_config("cache_dir"))
cache_file_path = os.path.join(caching_dir_path, get_from_config("cache_file"))


def initialize_cache_path():
    if not os.path.exists(caching_dir_path):
        os.makedirs(caching_dir_path)
    with open(cache_file_path, 'wb') as fp:
        pickle.dump({}, fp)


def clear_cache():
    if os.path.exists(caching_dir_path):
        shutil.rmtree(caching_dir_path)


class AbstractCacheableValue:
    def __init__(self, name, value, reimported=False):
        self.name = name
        self.value = value
        if reimported:
            self._import_myself()
        else:
            self._cache_myself()

    def _cache_myself(self):
        if not os.path.exists(cache_file_path):
            initialize_cache_path()
        pickle_object = None
        with open(cache_file_path, 'rb') as file:
            pickle_object = pickle.load(file)
        pickle_object[self.name] = self.value
        with open(cache_file_path, 'wb') as file:
            pickle.dump(pickle_object, file)

    def _import_myself(self):
        if not os.path.exists(cache_file_path):
            initialize_cache_path()
        with open(cache_file_path, 'rb') as file:
            pickle_object = pickle.load(file)
            self.value = pickle_object.get(self.name, self.value)


class CacheableDict(AbstractCacheableValue):
    def __contains__(self, item):
        self._import_myself()
        return item in self.value.keys()

    def __getitem__(self, item):
        self._import_myself()
        return self.value[item]

    def __setitem__(self, key, value):
        self._import_myself()
        self.value[key] = value
        self._cache_myself()

    def __len__(self):
        self._import_myself()
        return len(self.value)

    def keys(self):
        self._import_myself()
        return self.value.keys()


def get_item_from_cache(name):
    with open(cache_file_path, 'rb') as file:
        return pickle.load(file)[name]
