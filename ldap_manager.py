from loguru import logger as logging

from ldap3 import Server, Connection, ALL, SUBTREE, ALL_ATTRIBUTES
from ldap3.core.exceptions import LDAPCursorAttributeError, LDAPKeyError

from typing import List, Dict


def make_attribute_records(connection, master_attribute, description, attributes) -> List[Dict[str, str]]:
    result = []
    for user_record in connection.entries:
        try:
            user_common_name = user_record[master_attribute].value
            if user_common_name:
                logging.debug('___________________________')
                logging.debug(f'{description}: {user_common_name}')
                group_dict = {master_attribute: user_common_name}
                for attribute in attributes:
                    try:
                        logging.debug(f'Атрибут: {attribute} Значение: {user_record[attribute].value}')
                        group_dict[attribute] = user_record[attribute].value
                    except LDAPKeyError as ee:
                        logging.debug(f'Error: Значение {attribute} не найдено: {ee}')
                result.append(group_dict)
        except LDAPCursorAttributeError as e:
            logging.debug(f'Error: {e}')

    return result


class LdapManager:
    def __init__(self, hostname, username, password, base_dn):
        self._server = Server(hostname, get_info=ALL)
        self._username = username
        self._password = password
        self.scope = SUBTREE
        self.department = 'department'
        self.ldap_member_attr = 'sAMAccountName'
        self.ldap_search_attr = 'displayName'
        self.group_cn_param = 'cn'
        self.base_dn = base_dn

    def __enter__(self):
        self.connection = Connection(self._server, user=self._username, password=self._password, auto_bind=True)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.unbind()

    def get_groups_list(self, attributes=None) -> list:
        self.connection.search(self.base_dn, '(objectClass=group)', search_scope=self.scope, attributes=ALL_ATTRIBUTES)
        return make_attribute_records(self.connection, self.group_cn_param, 'Группа', attributes)

    def get_organizational_units(self):
        self.connection.search(self.base_dn, '(objectClass=organizationalUnit)', search_scope=self.scope)
        return [entry.ou.value for entry in self.connection.entries]

    def get_users_list(self, attributes=None) -> list:
        self.connection.search(self.base_dn,
                               '(&(objectClass=user)(!(objectClass=computer)))',
                               search_scope=self.scope,
                               attributes=ALL_ATTRIBUTES,
                               )
        return make_attribute_records(self.connection, self.ldap_member_attr, 'Пользователь', attributes)
