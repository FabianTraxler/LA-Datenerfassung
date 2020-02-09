import datetime

class Athlete_Handler():
    """Database Interface for all athlete specific agendas
    ...
    Attributes
    ----------
    DB_Handler: DB_Handler
        An Object wto interact with the database
    """
    def __init__(self, DB_Handler):
        """Constructor of the class
        ....
        Paramters
        ---------
        DB_Handler: DB_Handler
            A Class to interact with the Database
        """
        self.DB_Handler = DB_Handler
        self.group_disciplines_order = {
            "Decathlon": ['100-Meter', 'Weitsprung', 'Kugel-Stoßen', 'Hochsprung', '400-Meter', '110-Meter-Hürder', 'Diskus', 'Stabhochsprung', 'Speerwurf', '1500-Meter'],
            "Pethathlon": ['100-Meter', 'Weitsprung', 'Hochsprung', 'Speerwurf', '1200 Meter'],
            "Triathlon": ['60-Meter', 'Weitsprung', 'Schlagball']
        }
    
    def _get_age_group(self, birthday, gender):
        """Calculate the Age Group with  Birthday and Gender
        ...
        Paramters
        --------
        birthday: str
            String representation of the birthday (dd.mm.yyyyy)
        
        gender: str
            Gender as string (woman, man)

        Return
        -----
        str:
            age group as a string (eg. M40, W50, ...)
        """
        birth_year = int(birthday.split('.')[-1])
        year_difference = datetime.datetime.now().year - birth_year 
        gender_abbreviation = gender[0].upper() 

        if year_difference >= 60:
            age_group = gender_abbreviation + '60'
        elif year_difference >= 50:
            age_group = gender_abbreviation + '50'
        elif year_difference >= 40:
            age_group = gender_abbreviation + '40'
        elif year_difference <= 4:
            age_group = 'U4'
        elif year_difference <= 6:
            age_group = 'U6'
        elif year_difference <= 8:
            age_group = 'U8'
        elif year_difference <= 10:
            age_group = 'U8'
        elif year_difference <= 12:
            age_group = 'U12'
        elif year_difference <= 14:
            age_group = 'U14'
        elif year_difference <= 16:
            age_group = 'U16'
        
        else:
            age_group = gender_abbreviation
        
        return age_group

    def create_athlete(self, athlete_number, group_name, first_name, last_name, birthday, gender):
        """Create an Athlete and save the information in the database
        ...
        Paramters
        --------
        athlete_number: int
            Number of the Athlete
        group_name: str
            Name of the Group the Athlete is in
        first_name: str
            First Name
        last_name: str
            Last Name
        birthday: str
            String representation of the birthday (dd.mm.yyyyy)
        
        gender: str
            Gender as string (woman, man)
        """
        age_group = self._get_age_group(birthday, gender)
        if not group_name:
            group_name = age_group
        query = "INSERT INTO athletes VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(athlete_number, group_name, first_name, last_name, birthday, age_group, gender)
        if self.DB_Handler.commit_statement(query):
            return 1
        else:
            return 0

    def create_registered_athlete(self, group_name, first_name, last_name, birthday, gender):
        """Create an Athlete and save the information in the database
        ...
        Paramters
        --------
        group_name: str
            Name of the Group the Athlete is in
            If empty string --> Kids_Groups --> Group == Age_Group
        first_name: str
            First Name
        last_name: str
            Last Name
        birthday: str
            String representation of the birthday (dd.mm.yyyyy)
        gender: str
            Gender as string (woman, man)
        """

        age_group = self._get_age_group(birthday, gender)
        if not group_name:
            group_name = age_group
        query = "INSERT INTO registered_athletes VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(group_name, first_name, last_name, birthday, age_group, gender)
        if self.DB_Handler.commit_statement(query):
            return 1
        else:
            return 0

    def update_athlete(self, number, column, new_value):
        """Update the Database Entry of a existing athlete
        ...
        Paramters
        ---------
        athlete_number: int
            Number of the Athlete
        column: str
            Name of the column to be changed
        new_value: str
            New Value which should be inserted
        """
        query = "UPDATE athletes SET {} = '{}' WHERE number = {};".format(column, new_value, number)
        if column == 'birthday':
            gender = self.DB_Handler.get_result("SELECT age_group FROM athletes WHERE number = {};".format(number))[0][0]
            age_group = self._get_age_group(new_value, gender)
            query += "UPDATE athletes SET age_group = '{}' WHERE number = {};".format(age_group, number)
        if self.DB_Handler.commit_statement(query):
            return 1
        else:
            return 0

    def get_athletes(self, search_string):
        """Get all athletes which match the search string in first_ or last_name
        ...
        Paramters
        --------
        search_string: str
            String which is used for search
        
        Return
        ------
        list
            Returns a list of tuples with all the athletes found in the database
        """

        query = "SELECT * FROM athletes WHERE LOWER(first_name) LIKE LOWER('%{}%') OR LOWER(last_name) LIKE LOWER('%{}%');".format(search_string, search_string)
        rows = self.DB_Handler.get_results(query)
        return rows

    def get_registered_athletes(self, search_string):
        """Get all registered_athletes which match the search string in first_ or last_name
        ...
        Paramters
        --------
        search_string: str
            String which is used for search
        
        Return
        ------
        list
            Returns a list of tuples with all the athletes found in the database
        """

        query = "SELECT * FROM registered_athletes WHERE LOWER(first_name) LIKE LOWER('%{}%') OR LOWER(last_name) LIKE LOWER('%{}%');".format(search_string, search_string)
        rows = self.DB_Handler.get_results(query)
        return rows

    def get_athlete_performance(self, athlete_number):
        """Get the performance (best attemtpt + points) for every discipline for an athlete
        ...
        Paramters
        --------
        athlete_number: int
            Number of the Athlete
        Return
        ------
        list
            List of tuples with disciplines in normal order
        """
        query = "SELECT discipline_name, best_attempt, points  FROM achievements WHERE athlete_number = {}".format(athlete_number)
        performance = self.DB_Handler.get_results(query)

        return performance

