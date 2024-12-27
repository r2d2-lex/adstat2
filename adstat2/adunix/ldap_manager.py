from loguru import logger as logging

from ldap3 import Server, Connection, ALL, SUBTREE, ALL_ATTRIBUTES, MODIFY_REPLACE, MODIFY_DELETE
from ldap3.core.exceptions import LDAPCursorAttributeError, LDAPKeyError, LDAPAttributeError, LDAPInvalidValueError

from typing import List, Dict

GROUP_SEARCH_FILTER = '(objectClass=group)'
OU_SEARCH_FILTER = '(objectClass=organizationalUnit)'
USER_SEARCH_FILTER = '(objectClass=user)'
DEPARTMENT = 'department'
LDAP_MEMBER_ATTR = 'sAMAccountName'
LDAP_SEARCH_ATTR = 'displayName'
GROUP_CN_PARAM = 'cn'
USER_DN_PARAM = 'distinguishedName'


def make_attribute_records(connection, master_attribute, description, attributes) -> List[Dict[str, str]]:
    result = []
    for user_record in connection.entries:
        try:
            common_name = user_record[master_attribute].value
            if common_name:
                logging.debug(f'___________________________\r\n {description}: {common_name}')
                group_dict = {master_attribute: common_name}
                if attributes:
                    for attribute in attributes:
                        try:
                            logging.debug(f'Атрибут: {attribute} Значение: {user_record[attribute].value}')
                            group_dict[attribute] = user_record[attribute].value
                        except LDAPKeyError as ee:
                            logging.debug(f'Ошибка: Значение {attribute} не найдено: {ee}')
                            group_dict[attribute] = ''
                result.append(group_dict)
        except (LDAPCursorAttributeError, KeyError) as e:
            logging.debug(f'Ошибка: {e}')
    return result


def status_log(message, status_string):
    logging.info(message)
    status_string = status_string + '\r\n' + message
    status_string = status_string.lstrip('\r\n')
    return status_string


class LdapManager:
    def __init__(self, hostname, username, password, base_dn):
        self._server = Server(hostname, get_info=ALL)
        self._username = username
        self._password = password
        self.scope = SUBTREE
        self.base_dn = base_dn

    def __enter__(self):
        self.connection = Connection(self._server, user=self._username, password=self._password, auto_bind=True)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.unbind()

    def update_user_values(self, user_dn, attributes: dict, operation=None) -> (bool, str):
        status_string = ''
        result = False
        status_string = status_log(f'Изменение атрибутов для записи {user_dn}.', status_string)
        for attribute, value in attributes.items():
            try:
                if operation == MODIFY_DELETE:
                    self.connection.modify(user_dn, {attribute: [(MODIFY_DELETE, [])]})
                else:
                    self.connection.modify(user_dn, {attribute: [(MODIFY_REPLACE, [value])]})

                if self.connection.result['result'] == 0:
                    status_string = status_log(f'Атрибут {attribute} успешно изменен на {value}.', status_string)
                else:
                    status_string = status_log(f"Ошибка при изменении атрибута {attribute}: {self.connection.result['description']}",
                               status_string)
                    return result, status_string
            except (IndexError, KeyError, LDAPAttributeError, LDAPInvalidValueError) as err:
                status_string = status_log(f'Что-то пошло не так... Ошибка: {err}', status_string)
                return result, status_string
        result = True
        return result, status_string

    def get_groups_list(self, attributes=None) -> list:
        self.connection.search(self.base_dn, '(objectClass=group)', search_scope=self.scope, attributes=ALL_ATTRIBUTES)
        return make_attribute_records(self.connection, GROUP_CN_PARAM, 'Группа', attributes)

    def get_organizational_units(self):
        self.connection.search(self.base_dn, '(objectClass=organizationalUnit)', search_scope=self.scope)
        return [entry.ou.value for entry in self.connection.entries]

    def get_users(self) -> list:
        self.connection.search(self.base_dn,
                               '(&(objectClass=user)(!(objectClass=computer)))',
                               search_scope=self.scope,
                               attributes=ALL_ATTRIBUTES,
                               )
        return [entry for entry in self.connection.entries]

    def get_sam_user(self, sam_account_name, attributes) -> list:
        self.connection.search(self.base_dn,
                               '(sAMAccountName={})'.format(sam_account_name),
                               search_scope=self.scope,
                               attributes=ALL_ATTRIBUTES,
                               )
        return make_attribute_records(self.connection, LDAP_MEMBER_ATTR, 'Пользователь', attributes)

    def get_users_list(self, attributes=None) -> list:
        self.connection.search(self.base_dn,
                               '(&(objectClass=user)(!(objectClass=computer)))',
                               search_scope=self.scope,
                               attributes=ALL_ATTRIBUTES,
                               )
        return make_attribute_records(self.connection, LDAP_MEMBER_ATTR, 'Пользователь', attributes)
