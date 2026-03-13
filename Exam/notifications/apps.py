"""
Notifications app configuration.
"""

from django.apps import AppConfig
import logging

logger = logging.getLogger('app')


class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifications'
    verbose_name = 'Notifications'

    def ready(self):
        """Initialize signals and scheduler when Django starts"""
        import notifications.signals

        # Initialize exam reminder scheduler
        try:
            from .scheduler import get_scheduler
            get_scheduler()
            logger.info("Notifications app ready - exam reminder scheduler initialized")
        except Exception as e:
            logger.error(f"Error initializing scheduler: {str(e)}")
