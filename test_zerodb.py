from zerodb import ZeroDB
import time

db = ZeroDB()

# Set keys with and without TTL
db.set("username", "chatgpt")
db.set("session", "abc123", ttl=5)

print("All Keys:", db.keys())
print("Username:", db.get("username"))

time.sleep(6)

# Test expiration
try:
    print("Session:", db.get("session"))
except KeyError as e:
    print("Error:", e)

# Delete key
db.delete("username")

# Final keys
print("Keys after deletion:", db.keys())
