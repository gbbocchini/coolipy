"""Database models for the Coolify API."""

from __future__ import annotations

from datetime import datetime

from coolipy.models.base import CoolipyBaseModel


class DatabaseBaseModel(CoolipyBaseModel):
    """Shared fields for database create/update request bodies."""

    server_uuid: str | None = None
    project_uuid: str | None = None
    environment_name: str | None = None
    environment_uuid: str | None = None
    destination_uuid: str | None = None
    name: str | None = None
    description: str | None = None
    image: str | None = None
    is_public: bool | None = None
    public_port: int | None = None
    public_port_timeout: int | None = None
    limits_memory: str | None = None
    limits_memory_swap: str | None = None
    limits_memory_swappiness: int | None = None
    limits_memory_reservation: str | None = None
    limits_cpus: str | None = None
    limits_cpuset: str | None = None
    limits_cpu_shares: int | None = None
    instant_deploy: bool | None = None
    tags: list[str] | None = None
    postgres_user: str | None = None
    postgres_password: str | None = None
    postgres_db: str | None = None
    postgres_initdb_args: str | None = None
    postgres_host_auth_method: str | None = None
    postgres_conf: str | None = None
    clickhouse_admin_user: str | None = None
    clickhouse_admin_password: str | None = None
    dragonfly_password: str | None = None
    redis_password: str | None = None
    redis_conf: str | None = None
    keydb_password: str | None = None
    keydb_conf: str | None = None
    mariadb_conf: str | None = None
    mariadb_root_password: str | None = None
    mariadb_user: str | None = None
    mariadb_password: str | None = None
    mariadb_database: str | None = None
    mongo_conf: str | None = None
    mongo_initdb_root_username: str | None = None
    mongo_initdb_root_password: str | None = None
    mongo_initdb_database: str | None = None
    mysql_root_password: str | None = None
    mysql_password: str | None = None
    mysql_user: str | None = None
    mysql_database: str | None = None
    mysql_conf: str | None = None
    health_check_enabled: bool | None = None
    health_check_interval: int | None = None
    health_check_timeout: int | None = None
    health_check_retries: int | None = None
    health_check_start_period: int | None = None


class DatabaseModel(DatabaseBaseModel):
    """A database as returned by the API."""

    id: int | None = None
    uuid: str | None = None
    status: str | None = None
    environment_id: int | None = None
    server_id: int | None = None
    destination_id: int | None = None
    destination_type: str | None = None
    internal_db_url: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None


class DatabaseUpdateModel(DatabaseBaseModel):
    """Body for updating a database."""


class PostgreSQLModelCreate(DatabaseBaseModel):
    """Create a PostgreSQL database."""


class MySQLModelCreate(DatabaseBaseModel):
    """Create a MySQL database."""


class MariaDBModelCreate(DatabaseBaseModel):
    """Create a MariaDB database."""


class MongoDBModelCreate(DatabaseBaseModel):
    """Create a MongoDB database."""


class RedisModelCreate(DatabaseBaseModel):
    """Create a Redis database."""


class ClickhouseModelCreate(DatabaseBaseModel):
    """Create a ClickHouse database."""


class DragonflyModelCreate(DatabaseBaseModel):
    """Create a Dragonfly database."""


class KeyDBModelCreate(DatabaseBaseModel):
    """Create a KeyDB database."""


class DatabaseBackupCreate(CoolipyBaseModel):
    """Body for creating a scheduled backup configuration."""

    frequency: str | None = None
    enabled: bool | None = None
    save_s3: bool | None = None
    s3_storage_uuid: str | None = None
    databases_to_backup: str | None = None
    dump_all: bool | None = None
    backup_now: bool | None = None
    database_backup_retention_amount_locally: int | None = None
    database_backup_retention_days_locally: int | None = None
    database_backup_retention_max_storage_locally: float | None = None
    database_backup_retention_amount_s3: int | None = None
    database_backup_retention_days_s3: int | None = None
    database_backup_retention_max_storage_s3: float | None = None
    timeout: int | None = None
