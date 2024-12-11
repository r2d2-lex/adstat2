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
});