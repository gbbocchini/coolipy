from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Union

from models.base import CoolipyBaseModel


@dataclass
class TeamModel(CoolipyBaseModel):
    """
    Coolify Teams data model.
    """

    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    discord_enabled: Optional[bool] = None
    discord_notifications_database_backups: Optional[bool] = None
    discord_notifications_deployments: Optional[bool] = None
    discord_notifications_scheduled_tasks: Optional[bool] = None
    discord_notifications_server_disk_usage: Optional[bool] = None
    discord_notifications_status_changes: Optional[bool] = None
    discord_notifications_test: Optional[bool] = None
    discord_webhook_url: Optional[str] = None
    personal_team: Optional[bool] = None
    resend_api_key: Optional[str] = None
    resend_enabled: Optional[bool] = None
    show_boarding: Optional[bool] = None
    smtp_enabled: Optional[bool] = None
    smtp_encryption: Optional[str] = None
    smtp_from_address: Optional[str] = None
    smtp_from_name: Optional[str] = None
    smtp_host: Optional[str] = None
    smtp_notifications_database_backups: Optional[bool] = None
    smtp_notifications_deployments: Optional[bool] = None
    smtp_notifications_scheduled_tasks: Optional[bool] = None
    smtp_notifications_server_disk_usage: Optional[bool] = None
    smtp_notifications_status_changes: Optional[bool] = None
    smtp_notifications_test: Optional[bool] = None
    smtp_password: Optional[str] = None
    smtp_port: Optional[int] = None
    smtp_recipients: Optional[str] = None
    smtp_timeout: Optional[int] = None
    smtp_username: Optional[str] = None
    telegram_chat_id: Optional[int] = None
    telegram_enabled: Optional[bool] = None
    telegram_notifications_database_backups: Optional[bool] = None
    telegram_notifications_database_backups_message_thread_id: Optional[int] = None
    telegram_notifications_deployments: Optional[bool] = None
    telegram_notifications_deployments_message_thread_id: Optional[int] = None
    telegram_notifications_scheduled_tasks: Optional[bool] = None
    telegram_notifications_scheduled_tasks_thread_id: Optional[int] = None
    telegram_notifications_server_disk_usage: Optional[bool] = None
    telegram_notifications_status_changes: Optional[bool] = None
    telegram_notifications_status_changes_message_thread_id: Optional[int] = None
    telegram_notifications_test: Optional[bool] = None
    telegram_notifications_test_message_thread_id: Optional[int] = None
    telegram_token: Optional[str] = None
    use_instance_email_settings: Optional[bool] = None
    created_at: Optional[Union[str, datetime]] = None
    updated_at: Optional[Union[str, datetime]] = None


@dataclass
class TeamMemberModel(CoolipyBaseModel):
    """
    Coolify Team Members data model.
    """

    id: Optional[int] = None
    name: Optional[str] = None
    email: Optional[str] = None
    email_verified_at: Optional[Union[str, datetime]] = None
    force_password_reset: Optional[bool] = None
    marketing_emails: Optional[bool] = None
    two_factor_confirmed_at: Optional[Union[str, datetime]] = None
    created_at: Optional[Union[str, datetime]] = None
    updated_at: Optional[Union[str, datetime]] = None
