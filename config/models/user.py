from enum import IntEnum, auto


class CharactersOptions(IntEnum):
    ALPHA = auto()  # Only alphabetic characters allowed
    ALNUM = auto()  # Only alphanumeric characters allowed
    ALNUM_DASH_UNDERSCORE = auto()  # Only alphanumeric, dash and underscore characters allowed
    ANY = auto()  # Any character allowed


class UsernameOptions(IntEnum):
    MIN_LENGTH = 3
    MAX_LENGTH = 20
    CHARACTERS = CharactersOptions.ALNUM_DASH_UNDERSCORE


MIN_PASSWORD_LENGTH = 6
