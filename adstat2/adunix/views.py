from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from loguru import logger as logging
from .forms import UnixAttrsForm
from .ldap_manager import LdapManager, MODIFY_DELETE
from .utils import safe_int, make_errors_result


@staff_member_required
def update_user_data(request):
    result_message = 'Ошибка обновления данных'
    if request.method == 'POST':
        unix_form = UnixAttrsForm(request.POST)
        if unix_form.is_valid():
            unix_form_attrs = unix_form.cleaned_data
            distinguished_name = unix_form_attrs.get('distinguishedName', None)
            logging.debug(f'distinguished_name: {distinguished_name}')
            if distinguished_name:
                unix_attributes = {
                    'gidNumber': unix_form_attrs.get('gidNumber', None),
                    'uid': unix_form_attrs.get('uid', None),
                    'msSFU30Name': unix_form_attrs.get('msSFU30Name', None),
                    'msSFU30NisDomain': unix_form_attrs.get('msSFU30NisDomain', None),
                    'uidNumber': unix_form_attrs.get('uidNumber', None),
                    'loginShell': unix_form_attrs.get('loginShell', None),
                    'unixHomeDirectory': unix_form_attrs.get('unixHomeDirectory', None),
                }
                logging.debug(unix_attributes)
                with LdapManager(settings.LDAP_SERVER, settings.USERNAME, settings.PASSWORD,
                                 settings.BASE_DN_ROOT) as ldap_manger:
                    result, result_message = ldap_manger.update_user_values(distinguished_name, unix_attributes)
            return JsonResponse({'result': result_message})
        else:
            return JsonResponse({'result': make_errors_result(unix_form.errors)})
    return JsonResponse({'result': result_message}, status=400)


@staff_member_required
def delete_user_data(request):
    result_message = 'Ошибка удаления данных'
    if request.method == 'POST':
        distinguished_name = request.POST.get('distinguishedName', None)
        logging.debug(f'distinguished_name: {distinguished_name}')
        if distinguished_name:
            unix_attributes = {
                'gidNumber': None,
                'uid': None,
                'msSFU30Name': None,
                'msSFU30NisDomain': None,
                'uidNumber': None,
                'loginShell': None,
                'unixHomeDirectory': None,
            }
            with LdapManager(settings.LDAP_SERVER, settings.USERNAME, settings.PASSWORD,
                             settings.BASE_DN_ROOT) as ldap_manger:
                result, result_message = ldap_manger.update_user_values(
                    distinguished_name,
                    unix_attributes,
                    MODIFY_DELETE
                )
        return JsonResponse({'result': result_message})
    return JsonResponse({'result': result_message}, status=400)


@staff_member_required
def get_user_data(request):
    result = {
        'result_message': 'Ошибка загрузки данных',
        'result': False,
    }
    user_result = {}
    username = request.GET.get('username')
    with LdapManager(settings.LDAP_SERVER, settings.USERNAME, settings.PASSWORD, settings.BASE_DN_ROOT) as ldap_manger:
        attribute_list = ['cn', 'uid', 'msSFU30Name', 'msSFU30NisDomain', 'uidNumber', 'gidNumber', 'loginShell',
                          'unixHomeDirectory', 'distinguishedName']
        try:
            user_result = ldap_manger.get_sam_user(username, attribute_list)[0]
            if user_result:
                result = {
                    'result_message': 'Данные получены',
                    'result': True,
                }
        except IndexError:
            logging.debug('Что то пошло не так...')
    return JsonResponse({**result, **user_result})


@staff_member_required
def get_group_data(request):
    result = {
        'result_message': 'Ошибка загрузки данных',
        'result': False,
    }
    group_result = {}
    group_name = request.GET.get('groupname')
    logging.debug(f'group_name {group_name}')
    with LdapManager(settings.LDAP_SERVER, settings.USERNAME, settings.PASSWORD, settings.BASE_DN_ROOT) as ldap_manger:
        attribute_list = ['cn', 'msSFU30Name', 'msSFU30NisDomain', 'gidNumber', 'description']

        try:
            group_result = ldap_manger.get_sam_group(group_name, attribute_list)[0]
            if group_result:
                result = {
                    'result_message': 'Данные получены',
                    'result': True,
                }
        except IndexError:
            logging.debug('Что то пошло не так...')
    return JsonResponse({**result, **group_result})


@staff_member_required
def get_new_uid(request):
    with LdapManager(settings.LDAP_SERVER, settings.USERNAME, settings.PASSWORD, settings.BASE_DN_ROOT) as ldap_manger:
        attribute_list = ['uidNumber']
        users_result = ldap_manger.get_users_list(attribute_list)
        new_uid = max([safe_int(item.get('uidNumber', 0)) for item in users_result]) + 1
    return JsonResponse({'uidNumber': new_uid, 'domain': settings.DOMAIN})


@staff_member_required
def index(request):
    logging.debug(f'SETTINGS "{settings.LDAP_SERVER}", "{settings.USERNAME}", "{settings.PASSWORD}", "{settings.BASE_DN_ROOT}"')

    with LdapManager(settings.LDAP_SERVER, settings.USERNAME, settings.PASSWORD, settings.BASE_DN_ROOT) as ldap_manger:
        # Получение информации о группах
        attribute_list = ['gidNumber', 'description', 'sAMAccountName']
        group_result = ldap_manger.get_groups_list(attribute_list)
        group_result = sorted(group_result, key=lambda x: x['cn'])
        max_gid = max([safe_int(item.get('gidNumber', 0)) for item in group_result])

        # # Получение информации о пользователях
        attribute_list = ['cn', 'uidNumber']
        users_result = ldap_manger.get_users_list(attribute_list)
        users_result = sorted(users_result, key=lambda x: x['sAMAccountName'])
        max_uid = max([safe_int(item.get('uidNumber', 0)) for item in users_result])

        context = {
            'groups': group_result,
            'users': users_result,
            'max_uid': max_uid,
            'max_gid': max_gid,
        }
    return render(request, 'adunix/index.html', context)
