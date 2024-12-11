from django.shortcuts import render
from django.conf import settings
from loguru import logger as logging
import sys
from .ldap_manager import LdapManager, GROUP_SEARCH_FILTER, OU_SEARCH_FILTER, USER_SEARCH_FILTER


def index(request):
    logging.debug(f'SETTINGS "{settings.LDAP_SERVER}", "{settings.USERNAME}", "{settings.PASSWORD}", "{settings.BASE_DN_ROOT}"')

    with LdapManager(settings.LDAP_SERVER, settings.USERNAME, settings.PASSWORD, settings.BASE_DN_ROOT) as ldap_manger:
        attribute_list = ['gidNumber', 'description']
        group_result = ldap_manger.get_groups_list(attribute_list)

        context = {
            'groups': group_result,
        }
    return render(request, 'adunix/index.html', context)
