"""Tests utils"""
import unittest

from my_address_book.address_book import AddressBook as AB
from my_address_book.address_book import RecordContact
from my_address_book.entities import Email
from my_address_book.entities import Note
from my_address_book.entities import Phone
from my_address_book.entities import User
from my_address_book.notes_book import NotesBook as NB
from my_address_book.records import RecordNote
from my_address_book.utils import print_all_contacts
from my_address_book.utils import print_all_notes


class TestPrintContacts(unittest.TestCase):
    """Tests print all contacts"""

    def setUp(self) -> None:
        self.addressbook_test = AB()
        self.user_test = User("sasha")
        self.phone_test = Phone("380951234567")
        self.email_test = Email("test_sasha@gmail.com")
        self.record_test = RecordContact(self.user_test)

        self.notesbook_test = NB()
        self.note_test = Note("some text")
        self.record_note_test = RecordNote(self.note_test)
        self.name_note_test = "name note"

    def tearDown(self) -> None:
        del self.addressbook_test
        del self.record_test
        del self.user_test
        del self.phone_test
        del self.email_test

    def test_print_all_contacts_phone_email_true(self) -> None:
        """
        The test_print_all_contacts function tests the print_all_contacts function.
        It checks if the expected output is in the result of calling print_all_contacts.
        """
        self.record_test.add_phone_number(self.phone_test)
        self.record_test.add_email(self.email_test)
        self.addressbook_test.add_record(self.record_test)

        result = print_all_contacts(self.addressbook_test)
        expected_output = (
            "| sasha        | 380951234567              | test_sasha@gmail.com                 |    -     |        -         |"
        )

        self.assertTrue(expected_output in result)

    def test_print_all_contacts_phone_email_assignment_true(self) -> None:
        """
        The test_print_all_contacts function tests the print_all_contacts function.
        It checks if the expected output is in the result of calling print_all_contacts.
        """
        self.record_test.add_phone_number(self.phone_test, [0, "home"])
        self.record_test.add_email(self.email_test, [0, "home"])
        self.addressbook_test.add_record(self.record_test)

        result = print_all_contacts(self.addressbook_test)
        expected_output = (
            "| sasha        | 380951234567(home)        | test_sasha@gmail.com(home)           |    -     |        -         |"
        )

        self.assertTrue(expected_output in result)

    def test_print_all_contacts_phone_email_false(self) -> None:
        """
        The test_print_all_contacts function tests the print_all_contacts function.
        It checks if the expected output is in the result of calling print_all_contacts.
        """
        self.addressbook_test.add_record(self.record_test)

        result = print_all_contacts(self.addressbook_test)
        expected_output = (
            "| sasha        | -                         | -                                    |    -     |        -         |"
        )

        self.assertTrue(expected_output in result)

    def test_print_all_notes_name_false(self):
        self.notesbook_test.add_record(self.record_note_test)
        result = print_all_notes(self.notesbook_test)
        expected_output = "| 1 | -                     | some text                                                            | "
        self.assertTrue(expected_output in result)

    def test_print_all_notes_name_true(self):
        self.record_note_test.add_note_name(self.name_note_test)
        self.notesbook_test.add_record(self.record_note_test)
        result = print_all_notes(self.notesbook_test)
        expected_output = "| 1 | name note             | some text                                                            | "
        self.assertTrue(expected_output in result)


if __name__ == "__main__":
    unittest.main()
