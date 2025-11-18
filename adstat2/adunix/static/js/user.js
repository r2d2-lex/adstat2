const update_user_data = 'user_form';
const update_group_data = 'group_form';
const url_update_user_data = '/update_user_data/'

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

function showMessage(id, message, classAlert) {
    $(id).empty();
    let div = document.createElement('div');
    div.classList.add("alert");
    div.classList.add(classAlert);
    div.setAttribute("role", "alert");
    div.innerHTML = message;
    $(id).append(div);
}

function splitStringToListItems(inputString) {
    const lines = inputString.split('\n');
    const ul = document.createElement('ul');
    lines.forEach(line => {
        const li = document.createElement('li');
        li.textContent = line;
        ul.appendChild(li);
    });
    return ul.outerHTML;
}

function setGroupValue(groupID) {
    let $selectGroups = $('#groups');
    let status = false;
    $selectGroups.find('option').each(function() {
        if (Number($(this).val()) === groupID) {
            $(this).prop('selected', true);
            status = true;
            return false;
        }
    });
    if (!status) { $selectGroups.prop('selectedIndex', 0); }
}

function loadUserValues(username) {
    $.ajax({
        url: '/get_user_data/',
        data: {
            'username': username
        },
        dataType: 'json',
        success: function(data) {
            const result = data.result;
            const result_message = data.result_message;
            if (result === true) {
                showMessage('#result', 'Данные для пользователя: '+ data.sAMAccountName + ' успешно загружены!', 'alert-light');
                setGroupValue(data.gidNumber);
                $('#cn').val(data.cn);
                $('#sAMAccountName').val(data.sAMAccountName);
                $('#distinguishedName').val(data.distinguishedName);
                $('#gidNumber').val(data.gidNumber);
                $('#uid').val(data.uid);
                $('#msSFU30Name').val(data.msSFU30Name);
                $('#msSFU30NisDomain').val(data.msSFU30NisDomain);
                $('#uidNumber').val(data.uidNumber);
                $('#loginShell').val(data.loginShell);
                $('#unixHomeDirectory').val(data.unixHomeDirectory);
            } else {
                showMessage('#result', result_message, 'alert-danger');
            }
            console.log('Ajax get_user_data success');
        },
        error: function(xhr, status, error) {
            console.log('Ajax get_user_data error');
            console.error(error);
            showMessage('#result', 'Что то пошло не так!', 'alert-danger');
        }
    });
}

function loadGroupValues(groupname) {
    $.ajax({
        url: '/get_group_data/',
        data: {
            'groupname': groupname
        },
        dataType: 'json',
        success: function(data) {
            const result = data.result;
            const result_message = data.result_message;
            if (result === true) {
                showMessage('#result', 'Данные для группы: '+ data.sAMAccountName + ' успешно загружены!', 'alert-light');
                //setGroupValue(data.gidNumber);
                $('#grp_distinguishedName').val(data.distinguishedName);
                $('#grp_sAMAccountName').val(data.sAMAccountName);
                $('#grp_gidNumber').val(data.gidNumber);
                $('#grp_msSFU30Name').val(data.msSFU30Name);
                $('#grp_msSFU30NisDomain').val(data.msSFU30NisDomain);
                $('#grp_description').val(data.description);
            } else {
                showMessage('#result', result_message, 'alert-danger');
            }
            console.log('Ajax get_group_data success');
        },
        error: function(xhr, status, error) {
            console.log('Ajax get_group_data error');
            console.error(error);
            showMessage('#result', 'Что то пошло не так!', 'alert-danger');
        }
    });
}

$(document).ready(function() {

// ----------------------------- Карточка группы ----------------------------- //
    $('#grp_groups').change(function() {
        let groupname = $(this).val();
        if (groupname) {
            console.log('grp_groups');
            loadGroupValues(groupname);
        } else {
            // Очистка полей, если группа не выбрана
            $('#grp_distinguishedName').val('');
            $('#grp_sAMAccountName').val('');
            $('#grp_gidNumber').val('');
            $('#grp_msSFU30Name').val('');
            $('#grp_description').val('');
            $('#grp_msSFU30NisDomain').val('');
        }
    });
        // ---- Сохранение атрибутов
    $('#save_group').click(function() {
        $.ajax({
            url: url_update_user_data,
            type: 'POST',
            data: {
                'action': update_group_data,
                'distinguishedName': $('#grp_distinguishedName').val(),
                'gidNumber': $('#grp_gidNumber').val(),
                'msSFU30Name': $('#grp_msSFU30Name').val(),
                'msSFU30NisDomain': $('#grp_msSFU30NisDomain').val(),
                'description': $('#grp_description').val(),
                'csrfmiddlewaretoken': csrftoken,
            },
            success: function(response) {
                showMessage('#result', splitStringToListItems(response.result), 'alert-light');
                console.log('Ajax update_group_data success');
            },
            error: function(xhr, status, error) {
                console.log('Ajax update_group_data error');
                showMessage('#result', 'Что то пошло не так!', 'alert-danger');
            }
        });
    });


// ----------------------------- Карточка пользователя ----------------------------- //

    $('#users').change(function() {
        let username = $(this).val();
        if (username) {
            loadUserValues(username);
        } else {
            // Очистка полей, если пользователь не выбран
            $('#cn').val('');
            $('#sAMAccountName').val('');
            $('#distinguishedName').val('');
            $('#gidNumber').val('');
            $('#uid').val('');
            $('#msSFU30Name').val('');
            $('#msSFU30NisDomain').val('');
            $('#uidNumber').val('');
            $('#loginShell').val('');
            $('#unixHomeDirectory').val('');
        }
    });
    // ---- Назначение gidNumber
    $('#groups').change(function() {
        let gidNumber = $(this).val();
        if (gidNumber) {
            $('#gidNumber').val(gidNumber);
            } else {
            //
        }
    });
    // ---- Сохранение атрибутов
    $('#save').click(function() {
        $.ajax({
            url: url_update_user_data,
            type: 'POST',
            data: {
                'action': update_user_data,
                'distinguishedName': $('#distinguishedName').val(),
                'gidNumber': $('#gidNumber').val(),
                'uid': $('#uid').val(),
                'msSFU30Name': $('#msSFU30Name').val(),
                'msSFU30NisDomain': $('#msSFU30NisDomain').val(),
                'uidNumber': $('#uidNumber').val(),
                'loginShell': $('#loginShell').val(),
                'unixHomeDirectory': $('#unixHomeDirectory').val(),
                'csrfmiddlewaretoken': csrftoken,
            },
            success: function(response) {
                showMessage('#result', splitStringToListItems(response.result), 'alert-light');
                console.log('Ajax update_user_data success');
            },
            error: function(xhr, status, error) {
                console.log('Ajax update_user_data error');
                showMessage('#result', 'Что то пошло не так!', 'alert-danger');
            }
        });
    });
    // ---- Удаление атрибутов
    $('#delete').click(function() {
        $.ajax({
            url: '/delete_user_data/',
            type: 'POST',
            data: {
                'distinguishedName': $('#distinguishedName').val(),
                'csrfmiddlewaretoken': csrftoken,
            },
            success: function(response) {
                $('#exampleModal').modal('hide');
                showMessage('#result', splitStringToListItems(response.result), 'alert-warning');
                let username = $('#sAMAccountName').val();
                if (username) { loadUserValues(username); }
                console.log('Ajax delete_user_data success');
            },
            error: function(xhr, status, error) {
                console.log('Ajax delete_user_data error');
                showMessage('#result', 'Что то пошло не так!', 'alert-danger');
            }
        });
    });
    // ---- Заполнение unix атрибутов
    $('#fill').click(function() {
        let newUid = 0;
        $.ajax({
            url: '/get_new_uid/',
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrftoken,
            },
            success: function(response) {
                let userName = $('#sAMAccountName').val();
                const newUid = response.uidNumber;
                const domain = response.domain;
                console.log(response);
                if (userName) {
                    if ($('#gidNumber').val() == '') { $('#gidNumber').val(0); }
                    if ($('#uid').val() == '') { $('#uid').val(userName); }
                    if ($('#msSFU30Name').val() == '') { $('#msSFU30Name').val(userName); }
                    if ($('#msSFU30NisDomain').val() == '') { $('#msSFU30NisDomain').val(domain); }
                    if ($('#uidNumber').val() == '') { $('#uidNumber').val(newUid); }
                    if ($('#loginShell').val() == '') { $('#loginShell').val('/bin/bash'); }
                    if ($('#unixHomeDirectory').val() == '') { $('#unixHomeDirectory').val('/home/' + userName); }
                 }
                console.log('Ajax get_new_uid success');
                showMessage('#result', 'Данные успешно получены. Теперь можете сохранить новые атрибуты пользователя. Не забудьте назначить группу!', 'alert-light')
            },
            error: function(xhr, status, error) {
                console.log('Ajax get_new_uid error');
                showMessage('#result', 'Что то пошло не так!', 'alert-danger');
            }
        });
    });
    // ----
});