import requests


def getsub(get):
    CLIENT_ID = 'placeholder'
    SECRET_KEY = 'placeholder'

    print("Start ",get," Ende")

    # note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)

    # here we pass our login method (password), username, and password
    data = {'grant_type': 'password',
            'username': 'AitchBeeOfficial',
            'password': 'bibarmHR68'}

    # setup our header info, which gives reddit a brief description of our app
    headers = {'User-Agent': 'MyBot/0.0.1'}

    # send our request for an OAuth token
    res = requests.post('https://www.reddit.com/api/v1/access_token',
                        auth=auth, data=data, headers=headers)


    TOKEN = res.json()['access_token']

    # add authorization to our headers dictionary
    res = headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

    # print(res)
    # # while the token is valid (~2 hours) we just add headers=headers to our requests
    # requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)
    
    res = requests.get("https://oauth.reddit.com/r/"+get+"/about", headers = headers)

    #print(res.json()['data']['subscribers'])
    if 'data' in res.json():
            if'subscribers' in res.json()['data']:
                return int(res.json()['data']['subscribers'])
            else:
                return 0
        
    else:
            return 0
