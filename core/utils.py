from urllib.parse import unquote

from dj_database_url import parse as _database_parse
from storages.utils import safe_join


def generic_upload_to(base_path, instance, filename):
    """
    Just is possible use the ID as the filename where the table id is a UUIDField
    """
    assert(base_path is not None)

    ext = filename.split('.')[-1]
    filename = '%s.%s' % (instance.id, ext)

    return safe_join(base_path, filename)

def jwt_response_payload_handler(token, user=None, request=None):
    from users.serializers import UserSerializer
    return {
        'token': token,
        'user': UserSerializer(user).data if user.is_authenticated else None
    }

def database_parse(url, **kwargs):
    """
    dj_database_url.parse doesn't treat urlencoded in hostname, reparse database hostname
    """

    _parsed = _database_parse(url, **kwargs)

    return {
        **_parsed,
        'HOST': unquote(_parsed['HOST'])
    }
