import pytest
import re


@pytest.fixture
def get_data():
    page_content = '''
    <!DOCTYPE html>
    <html>
        <head>
            <!-- ... -->
        </head>
        <body>
            <script>
                window.init = {
                    "hosts": {
                        "host": "vk.com",
                        "api": "api.vk.com",
                        "id": "id.vk.com",
                        "login": "login.vk.com",
                        "oauth": "oauth.vk.com",
                        "domain": "vk.com"
                    },
                    "auth": {
                        "access_token": "access_token_test_example",
                        "anonymous_token": "anonymous_token_test_example",
                        "host_app_id": 6102407,
                        "auth_app_id": 0,
                        "user_id": 0
                    },
                    "params": {
                        "debug": false,
                        "origin": "",
                        "localhost": false,
                        "vkui_scheme": "space_gray"
                    }
                };
            </script>
        </body>
    </html>
    '''

    # Define the regular expression pattern
    pattern = r'"auth":\s*{\s*"(?:\w+|_\w+)"\s*:\s*"(.*?)",\s*"(?:\w+|_\w+)"\s*:\s*"(.*?)",\s*"(?:\w+|_\w+)"\s*:\s*([0-9]+),\s*"(?:\w+|_\w+)"\s*:\s*([0-9]+),\s*"(?:\w+|_\w+)"\s*:\s*([0-9]+)\s*}'

    # Find all matches using the regular expression
    matches = re.findall(pattern, page_content)

    return matches[0]


def test_auth_regexp(get_data):
    assert get_data == ('access_token_test_example', 'anonymous_token_test_example', '6102407', '0', '0')

