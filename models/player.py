class Player:

    def __init__(self, family_name, first_name, birth_date, national_id):
        self.family_name = family_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.national_id = national_id

    def __str__(self):
        return (f"{self.family_name} {self.first_name}, "
                f"né(e) le {self.birth_date}, ID: {self.national_id}")

    def __repr__(self):
         return f"{self.first_name} {self.family_name}"