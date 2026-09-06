from coolipy.enums import BuildPack, ProxyType, Redirect, ServiceType


def test_build_pack_includes_railpack():
    assert BuildPack.RAILPACK.value == "railpack"


def test_proxy_type_includes_none():
    assert ProxyType.NONE.value == "none"


def test_redirect_value_uses_hyphen():
    assert Redirect.NON_WWW.value == "non-www"


def test_service_type_value_uses_hyphen():
    assert ServiceType.WORDPRESS_WITH_MARIADB.value == "wordpress-with-mariadb"


def test_service_type_value_is_str():
    assert isinstance(ServiceType.N8N.value, str)
