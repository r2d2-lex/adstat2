from django.shortcuts import render
from django.conf import settings
from loguru import logger as logging
import sys
from .ldap_manager import LdapManager, GROUP_SEARCH_FILTER, OU_SEARCH_FILTER, USER_SEARCH_FILTER


def index(request):
    # logging.remove(0)
    logging.add(sys.stderr, level=settings.LOGGING_LEVEL)

    print(f'SETTINGS "{settings.LDAP_SERVER}", "{settings.USERNAME}", "{settings.PASSWORD}", "{settings.BASE_DN_ROOT}"')

    with LdapManager(settings.LDAP_SERVER, settings.USERNAME, settings.PASSWORD, settings.BASE_DN_ROOT) as ldap_manger:
        attribute_list = ['gidNumber', 'description']
        group_result = ldap_manger.get_groups_list(attribute_list)
        if group_result:
            for group in group_result:
                group_cn = group.get('cn')
                group_gid = group.get('gidNumber', '')
                group_description = group.get('description', '')
                print(f'Группа: {group_cn}, Gid: {group_gid}, Описание: {group_description}')

    return render(request, 'adunix/index.html')
