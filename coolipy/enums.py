"""Enums mirroring the string-constrained fields of the Coolify API.

Every member's :attr:`~enum.Enum.value` is the exact wire value the API expects
or returns, so serialize enums via ``.value`` (pydantic does this automatically
when models are dumped with ``mode="json"``).
"""

from __future__ import annotations

from enum import Enum


class BuildPack(str, Enum):
    """Build pack used to build an application."""

    NIXPACKS = "nixpacks"
    RAILPACK = "railpack"
    STATIC = "static"
    DOCKERFILE = "dockerfile"
    DOCKERCOMPOSE = "dockercompose"


class Redirect(str, Enum):
    """Domain redirect mode."""

    WWW = "www"
    NON_WWW = "non-www"
    BOTH = "both"


class ProxyType(str, Enum):
    """Reverse proxy used by a server."""

    TRAEFIK = "traefik"
    CADDY = "caddy"
    NONE = "none"


class DestinationType(str, Enum):
    """Network type of a destination."""

    STANDALONE = "standalone"
    SWARM = "swarm"


class ServiceType(str, Enum):
    """Known Coolify service types."""

    ACTIVEPIECES = "activepieces"
    APPSMITH = "appsmith"
    APPWRITE = "appwrite"
    AUTHENTIK = "authentik"
    BABYBUDDY = "babybuddy"
    BUDGE = "budge"
    CHANGEDETECTION = "changedetection"
    CHATWOOT = "chatwoot"
    CLASSICPRESS_WITH_MARIADB = "classicpress-with-mariadb"
    CLASSICPRESS_WITH_MYSQL = "classicpress-with-mysql"
    CLASSICPRESS_WITHOUT_DATABASE = "classicpress-without-database"
    CLOUDFLARED = "cloudflared"
    CODE_SERVER = "code-server"
    DASHBOARD = "dashboard"
    DIRECTUS = "directus"
    DIRECTUS_WITH_POSTGRESQL = "directus-with-postgresql"
    DOCKER_REGISTRY = "docker-registry"
    DOCUSEAL = "docuseal"
    DOCUSEAL_WITH_POSTGRES = "docuseal-with-postgres"
    DOKUWIKI = "dokuwiki"
    DUPLICATI = "duplicati"
    EMBY = "emby"
    EMBYSTAT = "embystat"
    FIDER = "fider"
    FILEBROWSER = "filebrowser"
    FIREFLY = "firefly"
    FORMBRICKS = "formbricks"
    GHOST = "ghost"
    GITEA = "gitea"
    GITEA_WITH_MARIADB = "gitea-with-mariadb"
    GITEA_WITH_MYSQL = "gitea-with-mysql"
    GITEA_WITH_POSTGRESQL = "gitea-with-postgresql"
    GLANCE = "glance"
    GLANCES = "glances"
    GLITCHTIP = "glitchtip"
    GRAFANA = "grafana"
    GRAFANA_WITH_POSTGRESQL = "grafana-with-postgresql"
    GROCY = "grocy"
    HEIMDALL = "heimdall"
    HOMEPAGE = "homepage"
    JELLYFIN = "jellyfin"
    JENKINS = "jenkins"
    KUZZLE = "kuzzle"
    LISTMONK = "listmonk"
    LOGTO = "logto"
    MEDIAWIKI = "mediawiki"
    MEILISEARCH = "meilisearch"
    METABASE = "metabase"
    METUBE = "metube"
    MINIO = "minio"
    MOODLE = "moodle"
    MOSQUITTO = "mosquitto"
    N8N = "n8n"
    N8N_WITH_POSTGRESQL = "n8n-with-postgresql"
    NEXT_IMAGE_TRANSFORMATION = "next-image-transformation"
    NEXTCLOUD = "nextcloud"
    NOCODB = "nocodb"
    ODOO = "odoo"
    OPENBLOCKS = "openblocks"
    PAIRDROP = "pairdrop"
    PENPOT = "penpot"
    PHPMYADMIN = "phpmyadmin"
    POCKETBASE = "pocketbase"
    POSTHOG = "posthog"
    REACTIVE_RESUME = "reactive-resume"
    ROCKETCHAT = "rocketchat"
    SHLINK = "shlink"
    SLASH = "slash"
    SNAPDROP = "snapdrop"
    STATUSNOOK = "statusnook"
    STIRLING_PDF = "stirling-pdf"
    SUPABASE = "supabase"
    SYNCTHING = "syncthing"
    TOLGEE = "tolgee"
    TRIGGER = "trigger"
    TRIGGER_WITH_EXTERNAL_DATABASE = "trigger-with-external-database"
    TWENTY = "twenty"
    UMAMI = "umami"
    UNLEASH_WITH_POSTGRESQL = "unleash-with-postgresql"
    UNLEASH_WITHOUT_DATABASE = "unleash-without-database"
    UPTIME_KUMA = "uptime-kuma"
    VAULTWARDEN = "vaultwarden"
    VIKUNJA = "vikunja"
    WEBLATE = "weblate"
    WHOOGLE = "whoogle"
    WORDPRESS_WITH_MARIADB = "wordpress-with-mariadb"
    WORDPRESS_WITH_MYSQL = "wordpress-with-mysql"
    WORDPRESS_WITHOUT_DATABASE = "wordpress-without-database"
