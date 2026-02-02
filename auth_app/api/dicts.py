from typing import TypedDict


class LoginUserDict(TypedDict):
    """
    Dictionary type for user login data.

    This typed dictionary defines the expected structure for
    login input, including:
    - username: the user's registered name
    - password: the user's password
    """

    username: str
    password: str
