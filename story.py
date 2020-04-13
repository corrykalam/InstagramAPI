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
        story_id = leertsefani.getStory()
        for story in story_id:
            print("Viewing story @%s"%(story["username"]))
            leertsefani.seenStory(story["reelid"], story["user_id"], story["taken_at"])
            time.sleep(random.randint(4, 7))
    except:
        print("Error!")
    print("Sleeping for 100 seconds")
    time.sleep(100)    