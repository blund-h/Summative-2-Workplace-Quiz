# Used for testing:
from quiz_utils import clean_name, check_valid_name


class TestSmoke:

    """ Confirms pytest is working as expected """

    def test_pytest_is_working(self):
        assert 6 + 7 == 13


class TestCleanName:

    """ Tests quiz_utils -> clean_name """

    def test_strips_whitespace(self):
        assert clean_name("  John  ") == "John"

    def test_title_cases(self):
        assert clean_name("john smith") == "John Smith"

    def test_already_clean(self):
        assert clean_name("John") == "John"


class TestCheckValidName:

    """ Tests quiz_utils -> check_valid_name """

    def test_valid_name(self):
        assert check_valid_name("John") == (True, "")

    def test_valid_name_with_hyphen(self):
        valid, _ = check_valid_name("John-Smith")
        assert valid is True

    def test_valid_name_with_spaces(self):
        valid, _ = check_valid_name("  John Smith  ")
        assert valid is True

    def test_empty_is_invalid(self):
        valid, msg = check_valid_name("")
        assert valid is False
        assert msg

    def test_whitespace_is_invalid(self):
        valid, _ = check_valid_name("   ")
        assert valid is False

    def test_50_chars_is_valid(self):
        valid, _ = check_valid_name("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAH")
        assert valid is True

    def test_51_chars_is_invalid(self):
        valid, msg = check_valid_name("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAH")
        assert valid is False
        assert msg

    def test_numbers_are_invalid(self):
        valid, msg = check_valid_name("John123")
        assert valid is False
        assert msg

    def test_special_characters_are_invalid(self):
        valid, msg = check_valid_name("John@PMO!")
        assert valid is False
        assert msg

    def test_single_character_valid(self):
        assert check_valid_name("X") == (True, "")


