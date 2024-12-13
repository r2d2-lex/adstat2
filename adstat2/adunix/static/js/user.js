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

function loadUserValues(username) {
    $.ajax({
        url: 'get_user_data',
        data: {
            'username': username
        },
        dataType: 'json',
        success: function(data) {
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
            showMessage('#result', 'Данные для пользователя: '+ data.sAMAccountName + ' успешно загружены!', 'alert-light');
        },
        error: function(xhr, status, error) {
            console.error(error);
        }
    });
}

$(document).ready(function() {
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
            url: '/update_user_data/',
            type: 'POST',
            data: {
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
                console.log('Ajax save success');
            },
            error: function(xhr, status, error) {
                console.log('Ajax save error');
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
                console.log('Ajax delete success');
            },
            error: function(xhr, status, error) {
                console.log('Ajax delete error');
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
            }
        });
    });
    // ----
});