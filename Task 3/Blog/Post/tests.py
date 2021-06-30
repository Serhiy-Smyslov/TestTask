from unittest import mock

from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import UserPost, SimpleUser, Comment
from .views import CreatePost, DeletePost, UpdatePost

User = get_user_model()


class BlogTestCases(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(username='testuser', password='password')
        image = SimpleUploadedFile('G60QvJ.jpg', content=b'', content_type='image/jpg')
        self.simple_user = SimpleUser.objects.create(name='NickName', user=self.user)
        self.post = UserPost.objects.create(
            title='Title1',
            content='Content1',
            image=image,
            author=self.simple_user
        )
        self.comment = Comment.objects.create(
            post=self.post,
            user=self.user,
            content='Content2'
        )

    def test_delete_post(self):
        factory = RequestFactory()
        request = factory.get('')
        request.user = self.user
        response = DeletePost.as_view()(request, pk=self.post.pk)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

    def test_mock_homepage(self):
        mock_data = mock.Mock(status_code=302)
        with mock.patch('Post.views.HomeView.get', return_value=mock_data) as mock_data_:
            factory = RequestFactory()
            request = factory.get('')
            request.user = self.user
            response = DeletePost.as_view()(request)
            self.assertEqual(response.status_code, 302)
