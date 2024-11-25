"""Utility functions for pydantic validation of the User model"""

from collections.abc import Callable

import pydantic as pyd

from config.models.user import MIN_PASSWORD_LENGTH, CharactersOptions, UsernameOptions

type Validator = Callable[[str, pyd.ValidationInfo], str]


def check_is_alphabetic(value: str, info: pyd.ValidationInfo) -> str:
    if not value.isalpha():
        raise ValueError(f"{info.field_name} must only contain letters")
    return value


def check_is_alphanumeric(value: str, info: pyd.ValidationInfo) -> str:
    if not value.isalnum():
        raise ValueError(f"{info.field_name} must only contain letters and numbers")
    return value


def check_is_alnum_dash_underscore(value: str, info: pyd.ValidationInfo) -> str:
    if not value.replace("-", "").replace("_", "").isalnum():
        raise ValueError(
            f"{info.field_name} must only contain letters, numbers, dashes and underscores"
        )
    return value


def username_validator_factory(options: type[UsernameOptions]) -> Validator:
    match options.CHARACTERS:
        case CharactersOptions.ALPHA:
            return check_is_alphabetic
        case CharactersOptions.ALNUM:
            return check_is_alphanumeric
        case CharactersOptions.ALNUM_DASH_UNDERSCORE:
            return check_is_alnum_dash_underscore
        case CharactersOptions.ANY:
            return lambda value, info: value
        case _:
            raise ValueError(
                f"Invalid characters option: {options.CHARACTERS} — "
                "please configure it in config/models/user.py"
            )


def check_username_length(value: str, info: pyd.ValidationInfo) -> str:
    if len(value) < UsernameOptions.MIN_LENGTH or len(value) > UsernameOptions.MAX_LENGTH:
        raise ValueError(
            f"{info.field_name} must be between {UsernameOptions.MIN_LENGTH} "
            f"and {UsernameOptions.MAX_LENGTH} characters long"
        )
    return value


def check_password_length(value: str, info: pyd.ValidationInfo) -> str:
    if len(value) < MIN_PASSWORD_LENGTH:
        raise ValueError(f"{info.field_name} must be at least 6 characters long")
    return value
