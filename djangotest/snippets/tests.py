from django.test import TestCase, Client, RequestFactory
from django.urls import resolve
from snippets.views import top, snippet_new, snippet_edit, snippet_detail
from django.contrib.auth import get_user_model
from snippets.models import Snippet

UserModel=get_user_model()

class TopPageRenderSnippetsTest(TestCase):  #トップページにスニペットが表示されるかのテスト
    def setUp(self):
        self.user=UserModel.objects.create(username='test_user', email="test@example.com", password='top_secret_pass0001') 
        self.snippet=Snippet.objects.create(title="title1", code="print('hello')", description="description1", created_by=self.user)

    def test_should_return_snippet_title(self):
        request=RequestFactory().get('/')
        request.user=self.user
        response=top(request)
        self.assertContains(response, self.snippet.title)

    def test_should_return_username(self):
        request=RequestFactory().get('/')
        request.user=self.user
        response=top(request)
        self.assertContains(response, self.user.username)       

class CreateSnippetTest(TestCase):  #スペニットの新規作成画面
    def test_should_resolve_snippet_new(self):
        found = resolve('/snippets/new/')
        self.assertEqual(snippet_new,found.func)

class SnippetDetailTest(TestCase):  #スペニットの詳細画面
    def test_should_resolve_snippet_detail(self):
        found = resolve('/snippets/1/')
        self.assertEqual(snippet_detail,found.func)

class EditSnippetTest(TestCase):  #スペニットの編集画面
    def test_should_resolve_snippet_edit(self):
        found = resolve('/snippets/1/edit/')
        self.assertEqual(snippet_edit,found.func)

#トップページが b"Hello, World" というプレーンテキストではなくHTMLファイルを返すように変更するため、
#TopPageViewTestクラスは削除して、TopPageTestクラスを次のように書き換え。

class TopPageTest(TestCase):  #トップページ
    def test_top_page_returns_200_and_expected_title(self):
        response = self.client.get('/')
        self.assertContains(response, "Djangoスニペット", status_code=200)

    def test_top_page_users_expected_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'snippets/top.html')