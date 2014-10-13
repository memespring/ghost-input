import unittest
import mock
import json
from app import app

class MockGhost:

    is_signed_in =  False

    def __init__(self, signed_in = False):
        self.is_signed_in = signed_in

    def signin(self, email, password):
        return True

    def get_drafts(self):
        text = '{"posts":[{"id":41,"uuid":"35a214d7-a144-437f-9f0b-66cf335236c6","title":"test title","slug":"test-title","markdown":"test content","html":"<p>test content</p>","image":null,"featured":false,"page":false,"status":"draft","language":"en_US","meta_title":null,"meta_description":null,"created_at":"2014-10-08T11:22:17.000Z","created_by":1,"updated_at":"2014-10-08T11:22:17.000Z","updated_by":1,"published_at":null,"published_by":null,"tags":[],"fields":[],"author":1}],"meta":{"pagination":{"page":1,"limit":15,"pages":1,"total":1,"next":null,"prev":null}}}'
        return json.loads(text)

    def get_post(self, post_id):
        result = self.get_drafts()
        return result['posts'][0]

    def save_post(self, post_id, title, markdown):
        return True

mock_ghost_signed_in = MockGhost(True)
mock_ghost_signed_out = MockGhost(False)

class GhostInputTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    @mock.patch('ghost.Ghost.signin', mock_ghost_signed_out.signin)
    def test_signin(self):

        rv = self.app.get('/signin')
        assert rv.status_code == 200

        rv = self.app.post('/signin', data={'email': 'test@example.org', 'password': 'example'})
        assert 'Redirecting' in rv.data

        rv = self.app.post('/signin', data={'email': '', 'password': ''})
        assert 'Invalid email address' in rv.data
        assert 'This field is required' in rv.data

    @mock.patch('ghost.Ghost.get_drafts', mock_ghost_signed_in.get_drafts)
    @mock.patch('ghost.Ghost.is_signed_in', mock_ghost_signed_in.is_signed_in)
    def test_view_drafts(self):
        rv = self.app.get('/')

        assert rv.status_code == 200
        assert 'test title' in rv.data

        assert rv.status_code == 200
        assert 'New post' in rv.data

    @mock.patch('ghost.Ghost.get_drafts', mock_ghost_signed_in.get_drafts)
    @mock.patch('ghost.Ghost.get_post', mock_ghost_signed_in.get_post)
    @mock.patch('ghost.Ghost.is_signed_in', mock_ghost_signed_in.is_signed_in)
    @mock.patch('ghost.Ghost.save_post', mock_ghost_signed_in.save_post)
    def test_edit_post(self):

        rv = self.app.get('/edit/1234')

        assert rv.status_code == 200
        assert 'test title' in rv.data

        rv = self.app.post('/edit/1234', data = {'title': 'test title', 'markdown': 'test content'})

        assert rv.status_code == 200

if __name__ == '__main__':
    unittest.main()
