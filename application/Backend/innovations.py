"""
innovations.py - Supporting module for AI features.
"""
import logging
import datetime

class KillSwitch:
    """A simple kill switch mechanism to disable certain AI functionalities."""
    def __init__(self):
        self._active = False
        logging.info("KillSwitch initialized.")

    def activate(self):
        """Activates the kill switch."""
        self._active = True
        logging.warning("KillSwitch has been ACTIVATED.")

    def deactivate(self):
        """Deactivates the kill switch."""
        self._active = False
        logging.info("KillSwitch has been deactivated.")

    def is_active(self):
        """Checks if the kill switch is active."""
        return self._active

class HeartStorage:
    """Handles persistent storage of critical AI insights in the SQLite database."""
    def __init__(self, db_conn):
        self.get_db = db_conn
    def store(self, user_id, insight):
        with self.get_db() as conn:
            conn.execute("INSERT INTO heart_storage (user_id, insight, created_at) VALUES (?, ?, ?)",
                         (user_id, insight, datetime.datetime.now().isoformat()))