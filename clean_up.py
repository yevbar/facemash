import json

obj = {}

with open("result.txt", 'r') as f:
    content = f.read()
    obj = json.loads(content)

bad_names = ['hunterwoodhall', 'MMeekerW', 'mcard1204', 'parkertracing', 'GreenKirken', 'PANYNJ', 'JeffMarkowitz1', 'AndrewParkerII', 'MatthewamHoward', 'Coach_Lim', 'swsandell', 'rambo_jordan', 'MrSteveAnderson', 'abigailxlovex', 'SteveRo67352623', 'TorresAdrianaTV', 'ProfGraceGu', 'KevinCarter_93']

for person in list(obj):
    print(obj[person])
    if obj[person]['screen_name'] in bad_names:
        del obj[person]
    elif obj[person]['profile_image_url_https'] == 'https://abs.twimg.com/sticky/default_profile_images/default_profile.png':
        del obj[person]
    elif 'football' in obj[person]['screen_name'].lower() or ('description' in obj[person] and 'football' in obj[person]['description'].lower()):
        del obj[person]
    else:
        try:
            if obj[person]['followers_count'] < 250:
                del obj[person]
        except:
            del obj[person]

with open('result.txt', 'w') as f:
    f.write(json.dumps(obj))
