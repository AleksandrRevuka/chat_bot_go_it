"""
entities module defines the entities used in the address book application.

Classes:
    Email: Represents the email of a contact.
        
    User: Represents a user.
        
    Phone: Represents the phone number of a contact.
    
"""


from datetime import datetime, date


class Email:
    """
    Represents the email of a contact.

    Attributes:
        email (str): The email address of the contact.

    Methods:
        __eq__(other: object) -> bool:
            Checks if the email address is equal to the email address of another Email object.

    """

    def __init__(self, email: str | None = None):
        self.email: str = email

    @property
    def email(self) -> str | None:
        """
        Returns the phone number of the contact.
        """
        return self.__email

    @email.setter
    def email(self, new_email: str) -> None:
        """
        The email function takes in a string and checks to see if it is a valid email address.
            If the email address is not valid, an error message will be returned.
            If the email address is valid, then it will return True.
        """
        if new_email is None:
            self.__email: str | None = None
        else:
            self.__email = new_email

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Email):
            return self.__email == other.email
        return False


class User:
    """
    Represents a user.

    Attributes:
        name (str): The name of the user.
        birthday_date (date | None): The birthday date of the user.

    """

    def __init__(self, name: str):
        self.__birthday_date: date | None = None
        self.name: str = name

    @property
    def name(self) -> str:
        """
        Returns the name of the contact.
        """
        return self.__name

    @name.setter
    def name(self, new_name: str) -> None:
        """
        Sets the name of the contact if it is valid, otherwise raises an error.
        """
        self.__name = new_name

    @property
    def birthday_date(self) -> date | None:
        """
        Returns the birthday date of the contact.
        """
        return self.__birthday_date

    @birthday_date.setter
    def birthday_date(self, new_birthday_date: datetime) -> None:
        """
        Sets the birthday date of the contact if it is valid, otherwise raises an error.
        """
        self.__birthday_date = new_birthday_date


class Phone:
    """
    Represents the phone number of a contact.

    Attributes:
        phone (str): The phone number of the contact.

    Methods:
        __eq__(other: object) -> bool:
            Checks if the phone number is equal to the phone number of another Phone object.

    """

    def __init__(self, phone: str | None = None):
        self.phone: str = phone

    @property
    def phone(self) -> str | None:
        """
        Returns the phone number of the contact.
        """
        return self.__phone

    @phone.setter
    def phone(self, new_phone: str) -> None:
        """
        Sets the phone number of the contact if it is valid, otherwise raises an error.
        """
        if new_phone is None:
            self.__phone: str | None = None
        else:
            self.__phone = new_phone

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Phone):
            return self.phone == other.phone
        return False


class Note:
    """
    A class that represents a note.

    Attributes:
        note (str | None): The content of the note.
        __name_note (str | None): The name of the note (private attribute).

    Methods:
        note() -> str | None:
            Returns the content of the note.
        note(new_note: str) -> None:
            Sets the content of the note.
        name_note() -> str | None:
            Returns the name of the note.
        name_note(new_name_note: str) -> None:
            Sets the name of the note.
    """

    def __init__(self, note: str | None = None):
        self.note: str = note
        self.__name_note: str | None = None

    @property
    def note(self) -> str | None:
        """
        The note function returns the note of a given instance of the class.
        """
        return self.__note

    @note.setter
    def note(self, new_note: str) -> None:
        """
        The note function takes a string and assigns it to the note attribute of an object.
        If no string is passed, then the note attribute is set to None.
        """

        if new_note is None:
            self.__note: str | None = None
        else:
            self.__note = new_note

    @property
    def name_note(self) -> str | None:
        """
        The name_note function returns the name of a note.
        """

        return self.__name_note

    @name_note.setter
    def name_note(self, new_name_note: str) -> None:
        """
        The name_note function takes a string as an argument and assigns it to the name_note attribute of the class.
        """

        self.__name_note = new_name_note
