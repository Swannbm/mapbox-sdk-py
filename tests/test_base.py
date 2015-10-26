import mapbox
import responses
import pytest
import requests


def test_service_session():
    """Get a session using a token"""
    session = mapbox.Service().get_session('pk.test')
    assert session.params.get('access_token') == 'pk.test'


def test_service_session_env():
    """Get a session using the env's token"""
    session = mapbox.Service().get_session(
        env={'MapboxAccessToken': 'pk.test_env'})
    assert session.params.get('access_token') == 'pk.test_env'


def test_service_session_os_environ(monkeypatch):
    """Get a session using os.environ's token"""
    monkeypatch.setenv('MapboxAccessToken', 'pk.test_os_environ')
    session = mapbox.Service().get_session()
    assert session.params.get('access_token') == 'pk.test_os_environ'
    monkeypatch.undo()


def test_service_session_os_environ_caps(monkeypatch):
    """Get a session using os.environ's token"""
    monkeypatch.setenv('MAPBOX_ACCESS_TOKEN', 'pk.test_os_environ')
    session = mapbox.Service().get_session()
    assert session.params.get('access_token') == 'pk.test_os_environ'
    monkeypatch.undo()


@responses.activate
def test_custom_messages():
    fakeurl = 'https://example.com'
    responses.add(responses.GET, fakeurl, status=401)
    service = mapbox.Service()
    response = service.get_session().get(fakeurl)

    assert service.handle_http_error(response) is None

    with pytest.raises(requests.exceptions.HTTPError) as exc:
        assert service.handle_http_error(response, custom_messages={401: "error"})
        assert exc.value.message == 'error'

    with pytest.raises(requests.exceptions.HTTPError) as exc:
        assert service.handle_http_error(response, raise_for_status=True)
        assert "401" in exc.value.message
