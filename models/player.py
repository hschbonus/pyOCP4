class Player:

    def __init__(self, lastname, firstname, birth_date, national_id):
        self.lastname = lastname
        self.firstname = firstname
        self.birth_date = birth_date
        self.national_id = national_id

    def __str__(self):
        return (f"{self.lastname} {self.firstname}, "
                f"né(e) le {self.birth_date}, ID: {self.national_id}")

    def __repr__(self):
        return f"{self.firstname} {self.lastname}"
