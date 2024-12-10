from loguru import logger as logging

from ldap3 import Server, Connection, ALL, SUBTREE, ALL_ATTRIBUTES
from ldap3.core.exceptions import LDAPCursorAttributeError, LDAPKeyError


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

    def get_groups_list(self, attributes=None):
        result = []
        self.connection.search(self.base_dn, '(objectClass=group)', search_scope=self.scope, attributes=ALL_ATTRIBUTES)

        for group_record in self.connection.entries:
            try:
                group_common_name = group_record[self.group_cn_param].value
                if group_common_name:
                    logging.debug('___________________________')
                    logging.debug(f'Группа: {group_common_name}')
                    group_dict = {self.group_cn_param: group_common_name}
                    for attribute in attributes:
                        try:
                            logging.debug(f'Атрибут: {attribute} Значение: {group_record[attribute].value}')
                            group_dict[attribute] = group_record[attribute].value
                        except LDAPKeyError as ee:
                            logging.debug(f'Error: Значение {attribute} не найдено: {ee}')
                    result.append(group_dict)
            except LDAPCursorAttributeError as e:
                logging.debug(f'Error: {e}')

        return result

    def get_organizational_units(self):
        self.connection.search(self.base_dn, '(objectClass=organizationalUnit)', search_scope=self.scope)
        return [entry.ou.value for entry in self.connection.entries]

    def get_users(self):
        self.connection.search(self.base_dn, '(objectClass=user)', search_scope=self.scope)
        return [entry.sAMAccountName.value for entry in self.connection.entries]
