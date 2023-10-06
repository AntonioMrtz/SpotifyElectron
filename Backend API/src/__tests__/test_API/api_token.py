from test_API.api_login import post_login
import pytest


def get_user_jwt_header(username : str , password : str):

    response = post_login(user_name=username,password=password)
    assert response.status_code==200

    jwt = response.json()

    return {
        "authorization": f"{jwt}",
    }
