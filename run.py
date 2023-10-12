from cryptography.fernet import Fernet


class Contact:
    def __init__(self, name, phone, email=None):
        self.name = name
        self.phone = phone
        self.email = email


class ContactSaver:
    def __init__(self):
        self.contacts = []
        self.password = None
        self.key = None

    def set_password(self, password):
        self.password = password
        self.key = Fernet.generate_key()
        print("Password set successfully!")

    def encrypt_data(self, data):
        fernet = Fernet(self.key)
        encrypted_data = fernet.encrypt(data.encode())
        return encrypted_data

    def decrypt_data(self, encrypted_data):
        fernet = Fernet(self.key)
        decrypted_data = fernet.decrypt(encrypted_data).decode()
        return decrypted_data

    def add_contact(self, name, phone, include_email=False):
        if self.password is None:
            print("Please set a password first!")
            return

        password_attempt = input("Enter the password to add a contact: ")
        if password_attempt != self.password:
            print("Incorrect password. Contact not saved.")
            return

        email = None
        if include_email:
            email = input("Enter the contact's email address: ")

        contact = Contact(name, phone, email)
        encrypted_name = self.encrypt_data(contact.name)
        encrypted_phone = self.encrypt_data(contact.phone)
        encrypted_email = self.encrypt_data(contact.email) if contact.email else None

        encrypted_contact = Contact(encrypted_name, encrypted_phone, encrypted_email)
        self.contacts.append(encrypted_contact)
        print("Contact saved successfully!")

    def view_contacts(self):
        if self.password is None:
            print("Please set a password first!")
            return

        password_attempt = input("Enter the password to view contacts: ")
        if password_attempt != self.password:
            print("Incorrect password. Contacts cannot be viewed.")
            return

        if not self.contacts:
            print("No contacts found.")
        else:
            print("Contacts:")
            for i, contact in enumerate(self.contacts, start=1):
                name = self.decrypt_data(contact.name)
                phone = self.decrypt_data(contact.phone)
                email = self.decrypt_data(contact.email) if contact.email else None
                print(f"{i}. Name: {name}, Phone: {phone}, Email: {email}")

    def search_contacts(self, term):
        if self.password is None:
            print("Please set a password first!")
            return

        password_attempt = input("Enter the password to search contacts: ")
        if password_attempt != self.password:
            print("Incorrect password. Contacts cannot be searched.")
            return

        found_contacts = []
        for contact in self.contacts:
            name = self.decrypt_data(contact.name)
            phone = self.decrypt_data(contact.phone)
            email = self.decrypt_data(contact.email) if contact.email else None

            if term.lower() in name.lower() or term.lower() in phone.lower() or (email and term.lower() in email.lower()):
                found_contacts.append((name, phone, email))

        if not found_contacts:
            print("No matching contacts found.")
        else:
            print("Matching Contacts:")
            for i, contact in enumerate(found_contacts, start=1):
                name, phone, email = contact
                print(f"{i}. Name: {name}, Phone: {phone}, Email: {email}")


contact_saver = ContactSaver()

while True:
    print("\n*** Contact Saver ***")
    print("1. Set Password")
    print("2. Add Contact")
    print("3. View Contacts")
    print("4. Search Contacts")
    print("5. Quit")

    choice = input("Enter your choice (1-5): ")

    if choice == '1':
        password = input("Enter the password: ")
        contact_saver.set_password(password)

    elif choice == '2':
        name = input("Enter the contact's name: ")
        phone = input("Enter the contact's phone number: ")
        include_email = input("Include email? (yes/no): ").lower() == "yes"
        contact_saver.add_contact(name, phone, include_email)

    elif choice == '3':
        contact_saver.view_contacts()

    elif choice == '4':
        term = input("Enter the search term: ")
        contact_saver.search_contacts(term)

    elif choice == '5':
        break

    else:
        print("Invalid choice. Please enter a number from 1 to 5.")

print("Thank you for using the Contact Saver. Goodbye!")
