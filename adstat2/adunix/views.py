from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from loguru import logger as logging
from .ldap_manager import LdapManager
from .utils import safe_int


def update_user_data(request):
    result_message = 'Ошибка обновления данных'
    if request.method == 'POST':
        distinguished_name = request.POST.get('distinguishedName', None)
        logging.debug(f'distinguished_name: {distinguished_name}')
        if distinguished_name:
            unix_attributes = {
                'gidNumber': request.POST.get('gidNumber', None),
                'uid': request.POST.get('uid', None),
                'msSFU30Name': request.POST.get('msSFU30Name', None),
                'msSFU30NisDomain': request.POST.get('msSFU30NisDomain', None),
                'uidNumber': request.POST.get('uidNumber', None),
                'loginShell': request.POST.get('loginShell', None),
                'unixHomeDirectory': request.POST.get('unixHomeDirectory', None),
            }
            logging.debug(unix_attributes)
            with LdapManager(settings.LDAP_SERVER, settings.USERNAME, settings.PASSWORD,
                             settings.BASE_DN_ROOT) as ldap_manger:
                result, result_message = ldap_manger.update_user_values(distinguished_name, unix_attributes)
        return JsonResponse({'result': result_message})
    return JsonResponse({'result': result_message}, status=400)


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
        attribute_list = ['cn', 'uidNumber']
        users_result = ldap_manger.get_users_list(attribute_list)
        users_result = sorted(users_result, key=lambda x: x['sAMAccountName'])
        max_uid = max([safe_int(item.get('uidNumber', 0)) for item in users_result])

        context = {
            'groups': group_result,
            'users': users_result,
            'max_uid': max_uid,
        }
    return render(request, 'adunix/index.html', context)
