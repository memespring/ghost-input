import requests
import json

class Ghost:

    access_token = None
    refresh_token = None

    @property
    def is_signed_in(self):
        return self.access_token != None

    def signin(self, email, password):
        #{"errors":[{"message":"Your password is incorrect.<br>4 attempts remaining!","type":"UnauthorizedError"}]}

        response = requests.post(
          'https://memespring.ghost.io/ghost/api/v0.1/authentication/token',
          {'grant_type': 'password', 'client_id': 'ghost-admin',  'username': email, 'password': password}
        )

        print response.status_code
        print response.text
        if response.status_code == 200:
            data = json.loads(response.text)
            self.access_token = data['access_token']
            self.refresh_token = data['refresh_token']
            return True
        else:
            return False

    def get_drafts(self):
        #https://github.com/TryGhost/Ghost/wiki/How-does-oAuth-work-with-Ghost%3F
        headers = {'Authorization': 'Bearer %s' % self.access_token}
        response = requests.get('https://memespring.ghost.io/ghost/api/v0.1/posts/?status=draft', headers=headers)
        return response.json()

    def get_post(self, post_id):
        headers = {'Authorization': 'Bearer %s' % self.access_token}
        response = requests.get('https://memespring.ghost.io/ghost/api/v0.1/posts/%s?status=draft' % str(post_id), headers=headers)
        posts = response.json()
        return posts['posts'][0]

    def create_post(self):

        headers = {'Authorization': 'Bearer %s' % self.access_token, 'content-type': 'application/json'}
        data = '{"posts":[{"title":"untitled","markdown":""}]}'
        response = requests.post('https://memespring.ghost.io/ghost/api/v0.1/posts',
                                headers=headers,
                                data=data
                              )
        posts = response.json()
        return posts['posts'][0]

    def save_post(self, post_id, title, markdown):

        #{"posts":[{"title":"test","slug":"test","markdown":"#test header\n\n\ntest content","html":"<h1 id=\"testheader\">test header</h1>\n\n<p>test content</p>","image":null,"featured":false,"page":false,"status":"draft","language":"en_US","meta_title":null,"meta_description":null,"author_id":1,"updated_at":"2014-09-17T16:00:49.000Z","published_at":null,"author":"1","published_by":null,"tags":[]}]}

        headers = {'Authorization': 'Bearer %s' % self.access_token, 'content-type': 'application/json'}
        post = self.get_post(post_id)
        post['title'] = title
        post['markdown'] = markdown
        data = json.dumps({'posts': [post]})
        response = requests.put('https://memespring.ghost.io/ghost/api/v0.1/posts/%s' % str(post_id),
                                headers=headers,
                                data=data
                              )
        print response
