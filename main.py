from ldap_manager import LdapManager
from loguru import logger as logging
import config
import sys

GROUP_SEARCH_FILTER = '(objectClass=group)'
OU_SEARCH_FILTER = '(objectClass=organizationalUnit)'
USER_SEARCH_FILTER = '(objectClass=user)'


def main():
    logging.remove(0)
    logging.add(sys.stderr, level=config.LOGGING_LEVEL)

    with LdapManager(config.LDAP_SERVER, config.USERNAME, config.PASSWORD, config.BASE_DN_ROOT) as ldap_manger:
        # # Получение информации о пользователях


        # # Получение информации о группах
        # attribute_list = ['gidNumber', 'description']
        # group_result = ldap_manger.get_groups_list(attribute_list)
        # if group_result:
        #     for group in group_result:
        #         group_cn = group.get('cn')
        #         group_gid = group.get('gidNumber', '')
        #         group_description = group.get('description', '')
        #         print(f'Группа: {group_cn}, Gid: {group_gid}, Описание: {group_description}')


if __name__ == '__main__':
    main()
