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
    def setUp(self):
        self.user=UserModel.objects.create(username='test_user', email="test@example.com", password="secret")
        self.client.force_login(self.user)
    
    def test_render_creation_form(self):
        response=self.client.get('/snippets/new/')
        self.assertContains(response, 'スニペットの登録',status_code=200)

    def test_create_snippet(self):
        data={'title':'タイトル', 'code':'コード', 'description':'解説'}
        self.client.post('/snippets/new/', data)
        snippet=Snippet.objects.get(title='タイトル')
        self.assertEqual('コード', snippet.code)
        self.assertEqual('解説', snippet.description)

class SnippetDetailTest(TestCase):  #スペニットの詳細画面
    def setUp(self):
        self.user=UserModel.objects.create(username='test_user', email="test@example.com", password="secret")
        self.snippet=Snippet.objects.create(title="タイトル", code="コード", description="解説", created_by=self.user)
    
    def test_should_use_expected_template(self):
        response=self.client.get(f'/snippets/%s/' % self.snippet.id)
        self.assertTemplateUsed(response, 'snippets/snippet_detail.html')

    def test_should_return_200_and_expected_heading(self):
        response=self.client.get(f'/snippets/%s/' % self.snippet.id)
        self.assertContains(response, self.snippet.title, status_code=200)

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