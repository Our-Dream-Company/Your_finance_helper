import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects, assertTemplateUsed
from authentication.forms import RegisterForm, LoginUserForm


@pytest.mark.parametrize('url, template', [
    ('login', 'authentication/login.html'),
    ('register', 'authentication/register.html')
])
@pytest.mark.django_db
def test_view_uses_correct_template_authentication(authenticated_user, url, template):
    resp = authenticated_user.get(reverse(url))
    assert resp.status_code == 200
    assertTemplateUsed(resp, template)


@pytest.mark.parametrize('url_form, form', [
    ('login', LoginUserForm),
    ('register', RegisterForm)
])
@pytest.mark.django_db
def test_correct_form_authentication(authenticated_user, url_form, form):
    response = authenticated_user.get(reverse(url_form))
    assert isinstance(response.context["form"], form)


@pytest.mark.django_db
def test_published_post_login(client, create_user):
    response_name = client.post(reverse('login'), {
        'username': 'john', 'password': 'Hack1234'})
    assertRedirects(response_name, reverse('main_page'))


@pytest.mark.django_db
def test_published_post_register(client):
    response_name = client.post(reverse('register'), {
        'username': 'john', 'email': 'lennon@thebeatles.com', 'password1': 'Hack1234', 'password2': 'Hack1234'})
    assertRedirects(response_name, reverse('main_page'))
