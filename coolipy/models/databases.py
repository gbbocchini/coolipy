from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Union, override
from coolipy.models.base import CoolipyBaseModel
from coolipy.models.servers import ServerModel


@dataclass
class DestinationModel(CoolipyBaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    uuid: Optional[str] = None
    network: Optional[str] = None
    server_id: Optional[int] = None
    created_at: Optional[Union[str, datetime]] = None
    updated_at: Optional[Union[str, datetime]] = None
    server: Optional[ServerModel] = field(default_factory=dict)

    @override
    def _adjust_nested(self):
        if isinstance(self.server, dict) and self.server:
            raw_server = self.server
            self.server = ServerModel(**raw_server).pythonify()


@dataclass
class DatabaseModel(CoolipyBaseModel):
    uuid: Optional[str] = None
    name: Optional[str] = None
    config_hash: Optional[str] = None
    custom_docker_run_options: Optional[str] = None
    database_type: Optional[str] = None
    deleted_at: Optional[Union[str, datetime]] = None
    description: Optional[str] = None
    destination: Optional[DestinationModel] = field(default_factory=dict)
    destination_id: Optional[int] = None
    destination_type: Optional[str] = None
    environment_id: Optional[int] = None
    external_db_url: Optional[str] = None
    image: Optional[str] = None
    init_scripts: Optional[str] = None
    internal_db_url: Optional[str] = None
    is_include_timestamps: Optional[bool] = None
    is_log_drain_enabled: Optional[bool] = None
    is_public: Optional[bool] = None
    last_online_at: Optional[str] = None
    limits_cpu_shares: Optional[int] = None
    limits_cpus: Optional[str] = None
    limits_cpuset: Optional[str] = None
    limits_memory: Optional[str] = None
    limits_memory_reservation: Optional[str] = None
    limits_memory_swap: Optional[str] = None
    limits_memory_swappiness: Optional[int] = None
    ports_mappings: Optional[str] = None
    clickhouse_admin_user: Optional[str] = None
    clickhouse_admin_password: Optional[str] = None
    dragonfly_password: Optional[str] = None
    postgres_conf: Optional[str] = None
    postgres_user: Optional[str] = None
    postgres_password: Optional[str] = None
    postgres_db: Optional[str] = None
    postgres_initdb_args: Optional[str] = None
    postgres_host_auth_method: Optional[str] = None
    mongo_conf: Optional[str] = None
    mongo_initdb_database: Optional[str] = None
    mongo_initdb_root_password: Optional[str] = None
    mongo_initdb_root_username: Optional[str] = None
    redis_conf: Optional[str] = None
    redis_password: Optional[str] = None
    postgres_db: Optional[str] = None
    keydb_password: Optional[str] = None
    keydb_conf: Optional[str] = None
    mariadb_conf: Optional[str] = None
    mariadb_conf: Optional[str] = None
    mariadb_root_password: Optional[str] = None
    mariadb_user: Optional[str] = None
    mariadb_password: Optional[str] = None
    mariadb_database: Optional[str] = None
    mysql_conf: Optional[str] = None
    mysql_root_password: Optional[str] = None
    mysql_user: Optional[str] = None
    mysql_database: Optional[str] = None
    postgres_host_auth_method: Optional[str] = None
    postgres_initdb_args: Optional[str] = None
    postgres_password: Optional[str] = None
    postgres_user: Optional[str] = None
    public_port: Optional[int] = None
    server_status: Optional[bool] = None
    started_at: Optional[Union[str, datetime]] = None
    status: Optional[str] = None
    created_at: Optional[Union[str, datetime]] = None
    updated_at: Optional[Union[str, datetime]] = None

    @override
    def _adjust_nested(self):
        if isinstance(self.destination, dict) and self.destination:
            raw_dest = self.destination
            self.destination = DestinationModel(**raw_dest).pythonify()


@dataclass
class DatabaseTypeCreateModelBase:
    server_uuid: str
    project_uuid: str
    environment_name: str
    name: str
    is_public: bool
    limits_memory: int
    limits_memory_swap: int
    limits_memory_swappiness: int
    limits_memory_reservation: int
    limits_cpus: int
    limits_cpu_shares: int
    instant_deploy: bool


@dataclass
class PostgreSQLModelCreate(DatabaseTypeCreateModelBase):
    postgres_user: str
    postgres_password: str
    postgres_db: str
    limits_cpu_shares: str
    postgres_initdb_args: str
    postgres_host_auth_method: str
    postgres_conf: str
    image: str = "postgresql"
    description: Optional[str] = None
    destination_uuid: Optional[str] = None
    public_port: Optional[int] = None
    limits_cpuset: Optional[str] = None


@dataclass
class ClickHouseModelCreate(DatabaseTypeCreateModelBase):
    clickhouse_admin_user: str
    clickhouse_admin_password: str
    image: str = "clickhouse"
    description: Optional[str] = None
    destination_uuid: Optional[str] = None
    public_port: Optional[int] = None
    limits_cpuset: Optional[str] = None


@dataclass
class DragonFlyModelCreate(DatabaseTypeCreateModelBase):
    dragonfly_password: str
    image: str = "chainguard/dragonfly"
    description: Optional[str] = None
    destination_uuid: Optional[str] = None
    public_port: Optional[int] = None
    limits_cpuset: Optional[str] = None


@dataclass
class RedisModelCreate(DatabaseTypeCreateModelBase):
    redis_password: str
    image: str = "redis"
    redis_conf: Optional[str] = None
    description: Optional[str] = None
    destination_uuid: Optional[str] = None
    public_port: Optional[int] = None
    limits_cpuset: Optional[str] = None


@dataclass
class KeyDBModelCreate(DatabaseTypeCreateModelBase):
    keydb_password: str
    image: str = "bitnami/keydb"
    keydb_conf: Optional[str] = None
    description: Optional[str] = None
    destination_uuid: Optional[str] = None
    public_port: Optional[int] = None
    limits_cpuset: Optional[str] = None


@dataclass
class MariaDBModelCreate(DatabaseTypeCreateModelBase):
    mariadb_root_password: str
    mariadb_user: str
    mariadb_password: str
    mariadb_database: str
    image: str = "mariadb"
    mariadb_conf: Optional[str] = None
    description: Optional[str] = None
    destination_uuid: Optional[str] = None
    public_port: Optional[int] = None
    limits_cpuset: Optional[str] = None


@dataclass
class MySQLModelCreate(DatabaseTypeCreateModelBase):
    mysql_root_password: str
    mysql_user: str
    mysql_database: str
    mysql_conf: Optional[str] = None
    image: str = "mysql"
    description: Optional[str] = None
    destination_uuid: Optional[str] = None
    public_port: Optional[int] = None
    limits_cpuset: Optional[str] = None


@dataclass
class MongoDBModelCreate(DatabaseTypeCreateModelBase):
    mongo_initdb_root_username: str
    mongo_conf: Optional[str] = None
    image: str = "mongo"
    description: Optional[str] = None
    destination_uuid: Optional[str] = None
    public_port: Optional[int] = None
    limits_cpuset: Optional[str] = None


@dataclass
class DatabaseUpdateModel:
    name: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    is_public: Optional[bool] = None
    public_port: Optional[int] = None
    limits_memory: Optional[str] = None
    limits_memory_swap: Optional[str] = None
    limits_memory_swappiness: Optional[int] = None
    limits_memory_reservation: Optional[str] = None
    limits_cpus: Optional[str] = None
    limits_cpuset: Optional[str] = None
    limits_cpu_shares: Optional[int] = None
    postgres_user: Optional[str] = None
    postgres_password: Optional[str] = None
    postgres_db: Optional[str] = None
    postgres_initdb_args: Optional[str] = None
    postgres_host_auth_method: Optional[str] = None
    postgres_conf: Optional[str] = None
    clickhouse_admin_user: Optional[str] = None
    clickhouse_admin_password: Optional[str] = None
    dragonfly_password: Optional[str] = None
    redis_password: Optional[str] = None
    redis_conf: Optional[str] = None
    keydb_password: Optional[str] = None
    keydb_conf: Optional[str] = None
    mariadb_conf: Optional[str] = None
    mariadb_root_password: Optional[str] = None
    mariadb_user: Optional[str] = None
    mariadb_password: Optional[str] = None
    mariadb_database: Optional[str] = None
    mongo_conf: Optional[str] = None
    mongo_initdb_root_username: Optional[str] = None
    mongo_initdb_root_password: Optional[str] = None
    mongo_initdb_init_database: Optional[str] = None
    mysql_root_password: Optional[str] = None
    mysql_user: Optional[str] = None
    mysql_database: Optional[str] = None
    mysql_conf: Optional[str] = None


DATABASE_TYPES_MAP = {
    PostgreSQLModelCreate: "postgresql",
    ClickHouseModelCreate: "clickhouse",
    DragonFlyModelCreate: "dragonfly",
    RedisModelCreate: "redis",
    KeyDBModelCreate: "keydb",
    MariaDBModelCreate: "mariadb",
    MySQLModelCreate: "mysql",
    MongoDBModelCreate: "mongodb",
}
