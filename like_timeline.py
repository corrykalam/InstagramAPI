from instagram_class import InstagramApi
import time, random
#loggin by token
# token = {'action': 'login', 'status': 'success', 'username': 'corrykalam', 'csrftoken': 'asdasfwjelkfwfw', 'sessionid': 'xjkcdjksxkdlsldsd'}
# get your token use function logIn()
# leertsefani = InstagramApi(session=token)


#login by user & password
leertsefani = InstagramApi("USERNAME", "PASSWORD")
leertsefani.logIn()
while(True):
    try:
        timeline_id = leertsefani.getHome()
        for like in timeline_id:
            leertsefani.likePost(like)
            time.sleep(random.randint(4, 7))
    except Exception as E:
        print(E)
        print("Error!")
    print("Sleeping for 100 seconds")
    time.sleep(100)    