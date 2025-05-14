import json
import os
import time

class ZeroDB:
    def __init__(self, filename="data.json"):
        self.filename = filename
        self._load()

    def _load(self):
        if not os.path.exists(self.filename):
            self.data = {}
        else:
            with open(self.filename, "r") as f:
                try:
                    self.data = json.load(f)
                except json.JSONDecodeError:
                    self.data = {}
        self._cleanup_expired()

    def _save(self):
        with open(self.filename, "w") as f:
            json.dump(self.data, f, indent=4)

    def _cleanup_expired(self):
        now = time.time()
        to_delete = []
        for key, value in self.data.items():
            if "ttl" in value and value["ttl"] is not None:
                if now - value["created_at"] > value["ttl"]:
                    to_delete.append(key)
        for key in to_delete:
            del self.data[key]
        if to_delete:
            self._save()

    def set(self, key, value, ttl=None):
        self.data[key] = {
            "value": value,
            "created_at": time.time(),
            "ttl": ttl  # in seconds
        }
        self._save()

    def get(self, key):
        self._cleanup_expired()
        if key in self.data:
            return self.data[key]["value"]
        raise KeyError(f"Key '{key}' not found or expired.")

    def delete(self, key):
        if key in self.data:
            del self.data[key]
            self._save()
        else:
            raise KeyError(f"Key '{key}' not found.")

    def keys(self):
        self._cleanup_expired()
        return list(self.data.keys())

    def clear(self):
        self.data = {}
        self._save()
