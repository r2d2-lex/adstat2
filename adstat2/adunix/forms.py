from django import forms


class UnixAttrsForm(forms.Form):
    distinguishedName = forms.CharField(label='distinguishedName')
    gidNumber = forms.IntegerField(label='gidNumber')
    uid = forms.CharField(label='uid')
    msSFU30Name = forms.CharField(label='msSFU30Name')
    msSFU30NisDomain = forms.CharField(label='msSFU30NisDomain')
    uidNumber = forms.IntegerField(label='uidNumber')
    loginShell = forms.CharField(label='loginShell')
    unixHomeDirectory = forms.CharField(label='unixHomeDirectory')
