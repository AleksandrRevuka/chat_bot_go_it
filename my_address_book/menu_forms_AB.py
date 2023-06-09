"""
The module provides the EditContactForm, DeleteContactForm, and AddContactForm classes for managing
contacts in an address book application.

Classes:
    EditContactForm(npyscreen.ActionPopup):
        A form for editing a contact's information.

    DeleteContactForm(npyscreen.ActionPopup):
        A form for deleting a contact from the address book.

    AddContactForm(npyscreen.ActionForm):
        A form for adding a new contact to the address book.

"""
from datetime import datetime

import npyscreen

from my_address_book.constants import FILE_AB
from my_address_book.entities import Email
from my_address_book.entities import Phone
from my_address_book.entities import User
from my_address_book.records import RecordContact
from my_address_book.utils import sanitize_phone_number
from my_address_book.validation import birthday_date_validation
from my_address_book.validation import check_name_in_address_book
from my_address_book.validation import check_name_not_in_address_book
from my_address_book.validation import email_validation
from my_address_book.validation import name_validation
from my_address_book.validation import phone_validation


class EditContactForm(npyscreen.ActionPopup):
    """
    A form class for editing contact information.

    This form allows the user to edit a contact's name. It checks if the entered name exists in the address book,
    displays a message if it does, and prompts the user to enter another name. If the name is valid,
    the form switches to the ADD CONTACT form to edit the contact.

    Attributes:
        contact_name_for_change (npyscreen.TitleText): The widget for entering the contact name.

    """

    def create(self) -> None:
        """
        The create function is called when the form is created.
        It sets up the widgets and their initial values.
        """
        self.contact_name_for_change = self.add(npyscreen.TitleText, name="Name")

    def beforeEditing(self) -> None:
        """
        The beforeEditing function is called before the form is displayed.
        It allows you to set up the form, and populate it with data from your object.
        The function takes no arguments, but has access to all of the widgets on your form.
        """
        self.contact_name_for_change.value = None

    def check_name(self) -> bool:
        """
        The check_name function checks to see if the name entered by the user is in
        the address book. If it is, then a message will be displayed and the user will
        be prompted to enter another name.
        """
        name = self.contact_name_for_change.value
        message = check_name_not_in_address_book(self.parentApp.addressbook, name)
        if message:
            npyscreen.notify_confirm(message, "Error", editw=1)
            self.contact_name_for_change.value = None
            return False
        return True

    def on_ok(self) -> None:
        """
        The on_ok function is called when the user presses enter on the form.
        It checks if a contact name has been entered, and if so, it passes that value to
        the ADD CONTACT form and switches to that form.
        """
        if self.check_name():
            self.parentApp.getForm("ADD CONTACT").value = self.contact_name_for_change.value
            self.parentApp.getForm("ADD CONTACT").name = "Edit contact"
            self.parentApp.switchForm("ADD CONTACT")

    def on_cancel(self) -> None:
        """
        The on_cancel function is called when the user presses ^C or ^Q.
        It switches back to the MAIN form.
        """
        self.parentApp.switchForm("MAIN")


class DeleteContactForm(npyscreen.ActionPopup):
    """
    A form class for deleting a contact.

    This form allows the user to enter the name of a contact to delete. It checks if the entered name exists
    in the address book and prompts the user to confirm the deletion. If confirmed, the contact is deleted
    from the address book and saved to file.

    Attributes:
        contact_name_for_del (npyscreen.TitleText): The widget for entering the contact name to delete.

    """

    def create(self) -> None:
        """
        The create function is called when the form is created.
        It sets up the widgets and their initial values.
        """
        self.contact_name_for_del = self.add(npyscreen.TitleText, name="Name")

    def beforeEditing(self) -> None:
        """
        The beforeEditing function is called before the form is displayed.
        It allows you to set up the form, and populate it with data from your object.
        The function takes no arguments, but has access to all of the widgets on your form.
        """
        self.contact_name_for_del.value = None

    def check_name(self) -> bool:
        """
        The check_name function is used to check if the name entered by the user
        is in the address book. If it is not, then a message will be displayed and
        the user will be prompted to enter another name.
        """

        name = self.contact_name_for_del.value
        message = check_name_not_in_address_book(self.parentApp.addressbook, name)
        if message:
            npyscreen.notify_confirm(message, "Error", editw=1)
            self.contact_name_for_del.value = None
            return False
        return True

    def delete_contact(self) -> str:
        """
        The delete_contact function is called when the user presses the 'Delete Contact' button.
        It deletes a contact from the address book, and saves it to file.
        """
        self.parentApp.addressbook.delete_record(self.contact_name_for_del.value)
        self.parentApp.addressbook.save_records_to_file(FILE_AB)
        return f"The contact '{self.contact_name_for_del.value}' has been deleted."

    def on_ok(self) -> None:
        """
        The on_ok function is called when the user presses enter on a form.
        It checks to see if the name entered by the user exists in our address book, and if it does,
        it deletes that contact from our address book.
        If not, then an error message is displayed.
        """
        respon = self.check_name()
        if respon:
            message = self.delete_contact()
            npyscreen.notify_confirm(message, "Delete!", editw=1)

            self.parentApp.switchForm("MAIN")

    def on_cancel(self) -> None:
        """
        The on_cancel function is called when the user presses ^C or ^Q.
        It will return to the previous form, which in this case is MAIN.
        """
        self.parentApp.switchForm("MAIN")


class AddContactForm(npyscreen.ActionForm):
    """
    This class represents a form for adding or editing a contact in an address book.

    Attributes:

        contact_name: npyscreen.TitleText -
            Widget for entering the contact's name.
        contact_phone_one: npyscreen.TitleText -
            Widget for entering the contact's first phone number.
        phone_assignment_one: npyscreen.TitleSelectOne -
            Widget for selecting the assignment of the first phone number.
        contact_phone_two: npyscreen.TitleText -
            Widget for entering the contact's second phone number.
        phone_assignment_two: npyscreen.TitleSelectOne -
            Widget for selecting the assignment of the second phone number.
        contact_phone_three: npyscreen.TitleText -
            Widget for entering the contact's third phone number.
        phone_assignment_three: npyscreen.TitleSelectOne -
            Widget for selecting the assignment of the third phone number.
        contact_email_one: npyscreen.TitleText -
            Widget for entering the contact's first email address.
        email_assignment_one: npyscreen.TitleSelectOne -
            Widget for selecting the assignment of the first email address.
        contact_email_two: npyscreen.TitleText -
            Widget for entering the contact's second email address.
        email_assignment_two: npyscreen.TitleSelectOne -
            Widget for selecting the assignment of the second email address.
        contact_birth_text: npyscreen.TitleText -
            Widget for entering the contact's birth year.
        contact_birth: npyscreen.TitleDateCombo -
            Widget for selecting the contact's birth date.

    Methods:

        create(): Sets up the form's widgets and their initial values.
        beforeEditing(): Populates the form with data from an existing contact before it is displayed.
        after_editing(): Resets the form's values after the user has finished editing.
        data_validation(): Validates the data entered by the user.
        _validate_phone_numbers(): Validates the phone numbers entered by the user.
        _validate_email_addresses(): Validates the email addresses entered by the user.
        _show_error_message(message, widget): Displays an error message to the user.
        while_editing(*args, **kwargs): Converts the entered birth year into a valid date format.
        add_contact(): Adds a new contact to the address book.
        _add_phone_numbers(contact): Adds phone numbers to the contact.
        _add_email_addresses(contact): Adds email addresses to the contact.
        change_contact(): Deletes the selected contact and adds a new contact with updated information.
        on_ok(): Handles the user's click on the OK button, validates the data, and adds or updates the contact.
        on_cancel(): Handles the user's click on the Cancel button, resets the form's values, and returns to the main form.
    """

    def create(self) -> None:
        """
        The create function is called when the form is created.
        It sets up the widgets and their initial values.
        """

        self.value = None
        self.contact_name: npyscreen.TitleText = self.add(npyscreen.TitleText, name="Name")
        self.contact_phone_one = self.add(npyscreen.TitleText, name="Number №1")
        self.phone_assignment_one = self.add(
            npyscreen.TitleSelectOne,
            scroll_exit=True,
            max_height=4,
            name="assignment",
            values=["home", "mobile", "work"],
        )
        self.contact_phone_two = self.add_widget(npyscreen.TitleText, name="Number №2")
        self.phone_assignment_two = self.add(
            npyscreen.TitleSelectOne,
            scroll_exit=True,
            max_height=4,
            name="assignment",
            values=["home", "mobile", "work"],
        )
        self.contact_phone_three = self.add_widget(npyscreen.TitleText, name="Number №3")
        self.phone_assignment_three = self.add(
            npyscreen.TitleSelectOne,
            scroll_exit=True,
            max_height=4,
            name="assignment",
            values=["home", "mobile", "work"],
        )

        self.contact_email_one = self.add(npyscreen.TitleText, name="Email №1")
        self.email_assignment_one = self.add(
            npyscreen.TitleSelectOne,
            scroll_exit=True,
            max_height=3,
            name="Email assignment",
            values=["home", "work"],
        )

        self.contact_email_two = self.add(npyscreen.TitleText, name="Email №2")
        self.email_assignment_two = self.add(
            npyscreen.TitleSelectOne,
            scroll_exit=True,
            max_height=3,
            name="Email assignment",
            values=["home", "work"],
        )

        self.contact_birth_text = self.add(npyscreen.TitleText, name="Year Birth:")
        self.contact_birth = self.add(
            npyscreen.TitleDateCombo,
            name="Date Birth:",
            date_format="%d-%m-%Y",
        )
        self.contact_birth.when_parent_changes_value = self.while_editing

    def beforeEditing(self) -> None:
        """
        The beforeEditing function is called before the form is displayed.
        It allows you to set up the form, and populate it with data from your object.
        The self argument refers to the Form itself, not a widget on it.
        """
        if self.value:
            record_contact: RecordContact = self.parentApp.addressbook.get_record(self.value)

            self.contact_name.value = record_contact.user.name

            if len(record_contact.phone_numbers) >= 1:
                self.contact_phone_one.value = (
                    record_contact.phone_numbers[0].subrecord.phone if record_contact.phone_numbers[0].subrecord.phone else None
                )
                self.phone_assignment_one.value = record_contact.phone_numbers[0].name

            if len(record_contact.phone_numbers) >= 2:
                self.contact_phone_two.value = (
                    record_contact.phone_numbers[1].subrecord.phone if record_contact.phone_numbers[1].subrecord.phone else None
                )
                self.phone_assignment_two.value = record_contact.phone_numbers[1].name

            if len(record_contact.phone_numbers) >= 3:
                self.contact_phone_three.value = (
                    record_contact.phone_numbers[2].subrecord.phone if record_contact.phone_numbers[2].subrecord.phone else None
                )
                self.phone_assignment_three.value = record_contact.phone_numbers[2].name

            if len(record_contact.emails) >= 1:
                self.contact_email_one.value = (
                    record_contact.emails[0].subrecord.email if record_contact.emails[0].subrecord.email else None
                )
                self.email_assignment_one.value = record_contact.emails[0].name

            if len(record_contact.emails) >= 2:
                self.contact_email_two.value = (
                    record_contact.emails[1].subrecord.email if record_contact.emails[1].subrecord.email else None
                )
                self.email_assignment_two.value = record_contact.emails[1].name

            self.contact_birth.value = record_contact.user.birthday_date

    def after_editing(self) -> None:
        """
        The afterEditing function is called after the user has finished editing a form.
        It allows you to perform any actions that are required, such as updating the database with new values.
        The function takes one argument: self, which is a reference to the form itself.
        """
        self.value = None
        self.contact_name.value = None

        self.contact_phone_one.value = None
        self.phone_assignment_one.value = None
        self.contact_phone_two.value = None
        self.phone_assignment_two.value = None
        self.contact_phone_three.value = None
        self.phone_assignment_three.value = None

        self.contact_email_one.value = None
        self.email_assignment_one.value = None
        self.contact_email_two.value = None
        self.email_assignment_two.value = None

        self.contact_birth_text.value = None
        self.contact_birth.value = None

        self.parentApp.getForm("ADD CONTACT").name = "Add contact"

    def data_validation(self) -> bool:
        """
        The data_validation function is used to validate the data entered by the user.
        It checks if all fields are filled in and if they contain valid information.
        If any of these conditions are not met, an error message will be displayed on screen.
        """
        name = self.contact_name.value
        message_error = name_validation(name)
        if message_error:
            self._show_error_message(message_error, self.contact_name)
            return False

        if self.value != name:
            message_error = check_name_in_address_book(self.parentApp.addressbook, name)
            if message_error:
                self._show_error_message(message_error, self.contact_name)
                return False

        if not self._validate_phone_numbers():
            return False

        if not self._validate_email_addresses():
            return False

        message_error = birthday_date_validation(self.contact_birth.value)
        if message_error:
            self._show_error_message(message_error, self.contact_birth_text)
            return False

        return True

    def _validate_phone_numbers(self) -> bool:
        """
        The _validate_phone_numbers function validates the phone numbers of a contact.
        """
        phone_widgets = [
            self.contact_phone_one,
            self.contact_phone_two,
            self.contact_phone_three,
        ]

        for phone_widget in phone_widgets:
            phone = phone_widget.value
            if phone:
                sanitized_phone = sanitize_phone_number(phone)
                message_error = phone_validation(sanitized_phone)
                if message_error:
                    self._show_error_message(message_error, phone_widget)
                    return False
                phone_widget.value = sanitized_phone

        return True

    def _validate_email_addresses(self) -> bool:
        """
        The _validate_email_addresses function validates the email addresses of a contact.
        """
        email_widgets = [self.contact_email_one, self.contact_email_two]

        for email_widget in email_widgets:
            email = email_widget.value
            if email:
                message_error = email_validation(email)
                if message_error:
                    self._show_error_message(message_error, email_widget)
                    return False

        return True

    def _show_error_message(self, message: str, widget: npyscreen.widget.Widget):
        """
        The _show_error_message function is a helper function that displays an error message to the user.
        It takes in two parameters: self and message. The self parameter is used for npyscreen widgets,
        and the message parameter is used to display an error message.
        """
        npyscreen.notify_confirm(message, "Error", editw=1)
        widget.value = None

    def while_editing(self, *args: list, **kwargs: dict) -> None:
        """
        The while_editing function is a function that allows the user to enter in a year for their birthday,
        and then it will automatically convert it into the date format.
        """
        if self.contact_birth_text.value:
            if not self.contact_birth.value:
                birthday = datetime.strptime(str(int(self.contact_birth_text.value)), "%Y").date()
                self.contact_birth.value = birthday

    def add_contact(self) -> str:
        """
        The add_contact function adds a contact to the address book.
        It takes in a self parameter, which is an instance of the AddContactForm class.
        The function returns a string that says &quot;The contact '{self.contact_name}' has been added&quot; if it succeeds.
        """
        user = User(self.contact_name.value)
        contact = RecordContact(user)

        self._add_phone_numbers(contact)
        self._add_email_addresses(contact)

        contact.add_birthday(self.contact_birth.value)

        self.parentApp.addressbook.add_record(contact)
        self.parentApp.addressbook.save_records_to_file(FILE_AB)
        return f"The contact '{self.contact_name.value}' has been added"

    def _add_phone_numbers(self, contact: RecordContact):
        """
        The _add_phone_numbers function is a helper function that adds phone numbers to the contact.
        It takes in two arguments: self and contact. The self argument is the current instance of the class,
        and it allows us to access attributes and methods within that class. The contact argument is an object
        of type RecordContact, which we will be adding phone numbers to.
        """
        phone_widgets = [
            (self.contact_phone_one, self.phone_assignment_one),
            (self.contact_phone_two, self.phone_assignment_two),
            (self.contact_phone_three, self.phone_assignment_three),
        ]

        for phone_widget, assignment_widget in phone_widgets:
            phone = phone_widget.value
            if phone:
                phone = Phone(phone)
                if assignment_widget.value:
                    assignment_value = [
                        assignment_widget.value[0],
                        assignment_widget.values[assignment_widget.value[0]],
                    ]
                    contact.add_phone_number(phone, assignment_value)
                else:
                    contact.add_phone_number(phone)

    def _add_email_addresses(self, contact: RecordContact):
        """
        The _add_email_addresses function is a helper function that adds email addresses to the contact.
        It takes in two parameters: self and contact. The self parameter is the current instance of the class,
        and it allows us to access attributes and methods defined within this class. The contact parameter is
        an object of type RecordContact, which represents a single record in our address book.
        """
        email_widgets = [
            (self.contact_email_one, self.email_assignment_one),
            (self.contact_email_two, self.email_assignment_two),
        ]

        for email_widget, assignment_widget in email_widgets:
            email = email_widget.value
            if email:
                email = Email(email)
                if assignment_widget.value:
                    assignment_value = [
                        assignment_widget.value[0],
                        assignment_widget.values[assignment_widget.value[0]],
                    ]
                    contact.add_email(email, assignment_value)
                else:
                    contact.add_email(email)

    def change_contact(self) -> str:
        """
        The function first deletes the selected contact, then calls add_contact() to create a new one
        with updated information.
        """
        self.parentApp.addressbook.delete_record(self.value)
        message = self.add_contact()
        message = f"The contact '{self.contact_name.value}' has been updated"
        return message

    def on_ok(self) -> None:
        """
        The on_ok function is called when the user presses OK on the form.
        It checks if all of the fields are valid, and then either adds a new contact or updates an existing one.
        If it's a new contact, it calls add_contact() to create a new record in AddressBook with all of its information;
        if it's an existing contact, change_contact() is called instead.
        """
        if self.data_validation():
            if not self.value:
                message = self.add_contact()
                self.after_editing()
                npyscreen.notify_confirm(message, "Saved!", editw=1)

            else:
                message = self.change_contact()
                self.after_editing()
                npyscreen.notify_confirm(message, "Saved!", editw=1)

            self.parentApp.switchForm("MAIN")

    def on_cancel(self) -> None:
        self.after_editing()
        self.parentApp.switchForm("MAIN")
