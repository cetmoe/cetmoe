base_url = '.battle.net'
base_api_url = '.api.blizzard.com'
base_openid_url = '.battle.net/oauth/.well-known/openid-configuration'


def form_url(region, *args):
    url = 'https://' + region + base_url
    for v in args:
        url += '/' + v
    return url


def form_api_url(region, *args):
    url = 'https://' + region + base_api_url
    for v in args:
        url += '/' + v
    return url


def form_openid_url(region):
    url = 'https://' + region + base_openid_url
    return url


def get_bnet(region, oauth_client):
    url = form_url(region, 'oauth/userinfo')
    resp = oauth_client.get(url)
    resp.raise_for_status()
    data = resp.json()
    return data['battletag']


def get_avatar(region, oauth_client, realm, name):
    url = form_api_url(region, 'profile/wow/character', realm, name, 'character-media')
    url = url + '?namespace=profile-eu&locale=en_US'
    resp = oauth_client.get(url)
    resp.raise_for_status()
    data = resp.json()
    for v in data['assets']:
        if v['key'] == 'avatar':
            return v['value']
