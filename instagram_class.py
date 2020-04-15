import requests, json, re, time

class InstagramApi:
    """
    created with <3 by corrykalam
    """
    def __init__(self, username=None, password=None, session={}):
        self.username = username
        self.password = password
        self.loggedIn = False
        self.session = session
        self.headers = {}
        self.base_url = "https://www.instagram.com"
        self.generateHeaders()
    def generateHeaders(self):
        if self.session == {}:
            headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 9; LM-G710 Build/PKQ1.181105.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.149 Mobile Safari/537.36'}
        else:
            headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 9; LM-G710 Build/PKQ1.181105.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.149 Mobile Safari/537.36'}
            headers["x-csrftoken"] = self.session["csrftoken"]
            headers["cookie"] = 'csrftoken='+self.session['csrftoken']+'; sessionid='+self.session['sessionid']
        self.headers = headers
    def unixTime(self):
        x = str(time.time())
        timenow = x.split(".")[0]
        return timenow
    def getStr(self, string,start,end, index=1):
        try:
            str = string.split(start)
            str = str[index].split(end)
            return str[0]
        except:
            return False
    def logIn(self):
        web_fetch = self.base_url+"/accounts/login/"
        web_login_url = self.base_url+"/accounts/login/ajax/"
        fetch_cookies = requests.get(web_fetch).headers
        csrf = self.getStr(str(fetch_cookies), 'csrftoken=', ';')
        mid = self.getStr(str(fetch_cookies), 'mid=', ';')
        headers = {
            'Host': 'www.instagram.com',
            'x-csrftoken': csrf,
            'user-agent': 'Mozilla/5.0 (Linux; Android 9; LM-G710 Build/PKQ1.181105.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.149 Mobile Safari/537.36',
            'cookie': 'rur=FTW; mid='+mid+'; csrftoken='+csrf,
        }
        data = {
            'username': self.username,
            'password': self.password
        }
        fetch_login = requests.post(web_login_url, headers=headers, data=data)
        if '{"authenticated": false' in fetch_login.text:
            data_login = {
                'action': 'login',
                'status': 'error',
                'username': self.username,
                'details': 'wrong username/password'
            }
        elif '{"authenticated": true' in fetch_login.text:
            print("You login as %s"%(self.username))
            self.loggedIn = True
            data_login = {
                'action': 'login',
                'status': 'success',
                'username': self.username,
                'csrftoken': self.getStr(str(fetch_login.headers), 'csrftoken=', ';'),
                'sessionid': self.getStr(str(fetch_login.headers), 'sessionid=', ';')
            }
            self.session = data_login
            self.headers["x-csrftoken"] = self.session["csrftoken"]
            self.headers["cookie"] = 'csrftoken='+self.session['csrftoken']+'; sessionid='+self.session['sessionid']
        else:
            data_login = fetch_login.text
        return data_login                
    def getHome(self):
        timeline_id = []
        post = requests.get(self.base_url, headers=self.headers)
        data_output = self.getStr(post.text, "window.__additionalDataLoaded('feed',", ");</script>")
        if data_output != False:
            json_timeline = json.loads(data_output)
            result = json_timeline["user"]["edge_web_feed_timeline"]
            for i in result["edges"]:
                if i["node"]["viewer_has_liked"] == False:
                    timeline_id.append(i["node"]["id"])
            return timeline_id
        else:
            print("You not loggedIn!")
            return False
    def getStory(self):
        story_id = []
        query_hash = self.getQueryHash()
        url = 'https://www.instagram.com/graphql/query/?query_hash=%s&variables={"reel_ids":[],"tag_names":[],"location_ids":[],"highlight_reel_ids":[],"precomposed_overlay":false,"show_story_viewer_list":true,"story_viewer_fetch_count":50,"story_viewer_cursor":"","stories_video_dash_manifest":false}'%(query_hash)
        post = requests.get(url, headers=self.headers)
        json_parse = json.loads(post.text)
        result = json_parse["data"]["user"]["feed_reels_tray"]["edge_reels_tray_to_reel"]
        for i in result["edges"]:
            user_id = i["node"]["id"]
            username = i["node"]["user"]["username"]
            if i["node"]["items"] != None:
                for b in i["node"]["items"]:
                    reelMediaId = b["id"]
                    taken_at = b["taken_at_timestamp"]
                    data_output = {
                        'reelid': reelMediaId,
                        'user_id': user_id,
                        'taken_at': str(taken_at),
                        'username': username
                    }
                    story_id.append(data_output)
        return story_id
    def seenStory(self, reelMediaId, user_id, taken_at):
        data = {
            'reelMediaId': reelMediaId,
            'reelMediaOwnerId': user_id,
            'reelId': user_id,
            'reelMediaTakenAt': taken_at,
            'viewSeenAt': self.unixTime()
        }
        post = requests.post(self.base_url+"/stories/reel/seen", headers=self.headers, data=data)
        status = json.loads(post.text)
        if status["status"] == "ok":
            print("Success seen story_id %s"%(reelMediaId))
            status_res = True
        else:
            print("Failed seen story_id %s"%(reelMediaId))
            status_res = False
        return status_res
    def follow(self, user_id):
        post = requests.post(self.base_url+"/web/friendships/%s/follow/"%(user_id), headers=self.headers)
        status = json.loads(post.text)
        if status["status"] == "ok":
            print("Success unfollow id %s"%(user_id))
            status_res = True
        else:
            print("Failed unfollow id %s"%(user_id))
            status_res = False
        return status_res
    def unfollow(self, user_id):
        post = requests.post(self.base_url+"/web/friendships/%s/unfollow/"%(user_id), headers=self.headers)
        status = json.loads(post.text)
        if status["status"] == "ok":
            print("Success unfollow id %s"%(user_id))
            status_res = True
        else:
            print("Failed unfollow id %s"%(user_id))
            status_res = False
        return status_res
    def likePost(self, id_post):
        post = requests.post(self.base_url+"/web/likes/%s/like/"%(id_post), headers=self.headers)
        status = json.loads(post.text)
        if status["status"] == "ok":
            print("Success like id %s"%(id_post))
            status_res = True
        else:
            print("Failed like id %s"%(id_post))
            status_res = False
        return status_res
    def unlikePost(self, id_post):
        post = requests.post(self.base_url+"/web/likes/%s/unlike/"%(id_post), headers=self.headers)
        status = json.loads(post.text)
        if status["status"] == "ok":
            print("Success unlike id %s"%(id_post))
            status_res = True
        else:
            print("Failed unlike id %s"%(id_post))
            status_res = False
        return status_res
    def findProfile(self, username):
        post = requests.get(self.base_url+"/%s/"%(username), headers=self.headers).text
        if "The link you followed may be broken, or the page may have been removed." in post:
            data_array = {
                'status': 'error',
                'details': 'user_not_found'
            }
        else:
            data_output = self.getStr(post, '<script type="text/javascript">window._sharedData = ', ';</script>')
            json_profile = json.loads(data_output)
            result = json_profile["entry_data"]["ProfilePage"][0]["graphql"]["user"]
            is_follow = result["followed_by_viewer"]
            is_private = result["is_private"]
            is_verified = result["is_verified"]
            is_follback = result["follows_viewer"]
            user_id = result["id"]
            followers = result["edge_followed_by"]["count"]
            following = result["edge_follow"]["count"]
            data_array= {
                'status': 'success',
                'user_id': user_id,
                'username': username,
                'is_follow': is_follow,
                'is_private': is_private,
                'is_verifed': is_verified,
                'is_follback': is_follback,
            }
        return data_array
    def getQueryHash(self):
        post = requests.get(self.base_url, headers=self.headers)
        query_hash = self.getStr(post.text, '/graphql/query/?query_hash=', '&amp;', 1)
        return query_hash
    def getStoryIds(self, session, limit=False):
        url = "https://www.instagram.com/"
        reel_id = []
        headers = {
            'Host': 'www.instagram.com',
            'x-csrftoken': session["csrftoken"],
            'user-agent': 'Mozilla/5.0 (Linux; Android 9; LM-G710 Build/PKQ1.181105.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.149 Mobile Safari/537.36',
            'cookie': 'csrftoken='+session['csrftoken']+'; sessionid='+session['sessionid']
        }
        post = requests.get(url, headers=headers)
        getting_link = self.getStr(post.text, '<link rel="preload" href="/graphql/', '" as="fetch" type="application/json" crossorigin />')
        fething_story = url+"graphql/"+ getting_link.replace("&amp;", "&")
        fetch_story = requests.get(fething_story, headers=headers).text
        json_story = json.loads(fetch_story)
        result = json_story["data"]["user"]["feed_reels_tray"]["edge_reels_tray_to_reel"]["edges"]
        if limit == False:
            for items in result:
                try:
                    reelid = items["node"]["id"]
                    reel_id.append(reelid)
                except: pass
            output_fetch = json.dumps(reel_id)
        else:
            for i in range(int(limit)):
                try:
                    reelid = result[i]["node"]["id"]
                    reel_id.append(reelid)
                except: pass
            output_fetch = json.dumps(reel_id)
        return output_fetch
