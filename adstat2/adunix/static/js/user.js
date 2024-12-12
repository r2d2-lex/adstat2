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
console.log('CSRF: '+ csrftoken);

$(document).ready(function() {
    $('#users').change(function() {
        let username = $(this).val();
        if (username) {
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
                },
                error: function(xhr, status, error) {
                    console.error(error);
                }
            });
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

    $('#groups').change(function() {
        let gidNumber = $(this).val();
        if (gidNumber) {
            $('#gidNumber').val(gidNumber);
            } else {
            //
        }
    });
    // ----
    $('#save').click(function() {
        var data = {
            distinguishedName: $('#distinguishedName').val(),
            gidNumber: $('#gidNumber').val(),
            uid: $('#uid').val(),
            msSFU30Name: $('#msSFU30Name').val(),
            msSFU30NisDomain: $('#msSFU30NisDomain').val(),
            uidNumber: $('#uidNumber').val(),
            loginShell: $('#loginShell').val(),
            unixHomeDirectory: $('#unixHomeDirectory').val(),
        };
        console.log(data);
        $.ajax({
            url: '/update_user_data/',
            type: 'POST',
            data: data,
            dataType: 'json',
            beforeSend: function(xhr) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    },
            success: function(response) {
                $('#result').text(response.result);
                console.log('Всё хорошо');
                console.log(response.result);
            },
            error: function(xhr, status, error) {
                $('#result').text('Ошибка: ' + error);
                console.log('Ошибка');
                console.log(response.result);
                console.log('Ошибка');
        console.log(xhr.responseText);
            }
        });
    });
    // ----
});