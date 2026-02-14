"""キャッシュ管理（JSON形式）"""

import json
import os
import shutil


CACHE_DIR = os.path.join(os.path.dirname(__file__), "cache")


class CacheManager:
    def __init__(self, enabled: bool = True, cache_dir: str = CACHE_DIR):
        self.enabled = enabled
        self.cache_dir = cache_dir
        if enabled:
            os.makedirs(cache_dir, exist_ok=True)

    def _path(self, category: str, key: str) -> str:
        safe_key = key.replace("/", "_").replace("\\", "_")
        category_dir = os.path.join(self.cache_dir, category)
        os.makedirs(category_dir, exist_ok=True)
        return os.path.join(category_dir, f"{safe_key}.json")

    def get(self, category: str, key: str):
        if not self.enabled:
            return None
        path = self._path(category, key)
        if not os.path.exists(path):
            return None
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def set(self, category: str, key: str, value):
        if not self.enabled:
            return
        path = self._path(category, key)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(value, f, ensure_ascii=False, indent=2)

    def clear(self, ncode: str | None = None):
        """キャッシュを削除する

        ncode指定時: そのncodeに関連するキャッシュのみ削除
        ncode未指定時: 全キャッシュを削除
        """
        if not os.path.exists(self.cache_dir):
            return
        if ncode is None:
            shutil.rmtree(self.cache_dir)
            return
        safe_ncode = ncode.replace("/", "_").replace("\\", "_")
        for category in os.listdir(self.cache_dir):
            category_dir = os.path.join(self.cache_dir, category)
            if not os.path.isdir(category_dir):
                continue
            for filename in os.listdir(category_dir):
                if filename.startswith(safe_ncode):
                    os.remove(os.path.join(category_dir, filename))
