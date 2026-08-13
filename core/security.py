import time

def verify_owner(sender_id, owner_id):
    if not sender_id or not owner_id:
        return False
    return str(sender_id).strip() == str(owner_id).strip()

class RateLimiter:
    def __init__(self, cooldown_seconds=1.0):
        self.cooldown_seconds = cooldown_seconds
        self.last_calls = {}

    def is_allowed(self, user_id):
        now = time.time()
        last = self.last_calls.get(user_id, 0)
        if now - last < self.cooldown_seconds:
            return False
        self.last_calls[user_id] = now
        return True
