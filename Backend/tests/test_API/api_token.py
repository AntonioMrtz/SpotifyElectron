from starlette.status import HTTP_200_OK

from tests.test_API.api_login import post_login


def get_user_jwt_header(username: str, password: str) -> dict[str, str]:
    response = post_login(user_name=username, password=password)
    assert response.status_code == HTTP_200_OK

    jwt = response.json()

    return {
        "authorization": f"Bearer {jwt}",
    }
