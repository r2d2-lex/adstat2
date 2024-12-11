from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from loguru import logger as logging
from .ldap_manager import LdapManager


def get_user_data(request):
    username = request.GET.get('username')
    with LdapManager(settings.LDAP_SERVER, settings.USERNAME, settings.PASSWORD, settings.BASE_DN_ROOT) as ldap_manger:
        attribute_list = ['cn', 'uid', 'msSFU30Name', 'msSFU30NisDomain', 'uidNumber', 'gidNumber', 'loginShell',
                          'unixHomeDirectory', 'distinguishedName']
        try:
            users_result = ldap_manger.get_sam_user(username, attribute_list)[0]
        except IndexError:
            logging.debug('Что то пошло не так...')
    return JsonResponse(users_result)


def index(request):
    logging.debug(f'SETTINGS "{settings.LDAP_SERVER}", "{settings.USERNAME}", "{settings.PASSWORD}", "{settings.BASE_DN_ROOT}"')

    with LdapManager(settings.LDAP_SERVER, settings.USERNAME, settings.PASSWORD, settings.BASE_DN_ROOT) as ldap_manger:
        # Получение информации о группах
        attribute_list = ['gidNumber', 'description']
        group_result = ldap_manger.get_groups_list(attribute_list)
        group_result = sorted(group_result, key=lambda x: x['cn'])

        # # Получение информации о пользователях
        attribute_list = ['cn',]
        users_result = ldap_manger.get_users_list(attribute_list)
        users_result = sorted(users_result, key=lambda x: x['sAMAccountName'])

        context = {
            'groups': group_result,
            'users': users_result,
        }
    return render(request, 'adunix/index.html', context)
