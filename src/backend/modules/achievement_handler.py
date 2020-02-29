class Achievement_Handler():
    """Database Interface for all achievement specific agendas
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
        self.calculator = Points_Calculator()
    
    def store_attempt(self, athlete_number, group_name, discipline_name, attempt):
        """Store an attempt in the database
        ...
        Paramters
        --------
        athlete_number: int
            Number of the Athlete
        group_name: str
            Name of the group
        discipline_name: str
            Name of the discipline
        attempt: str
            String representation of the attempt to store in DB
        """

        # Get already stored attempts
        query = "SELECT attempts FROM achievements WHERE athlete_number = {} AND discipline_name = '{}'".format(athlete_number, discipline_name)
        result = self.DB_Handler.get_result(query)

        if discipline_name == 'Hochsprung' or discipline_name == 'Stabhochsprung':
            # check how many jumps since last height increase
            nr_jumps = len(result[0]) - result[0].find('/')
            attempts = result[0]
            if attempt == 'O' or attempt == '-':
                attempts +=  attempt + '/'
            elif attempt == 'X':
                attempts +=  attempt
            query = "UPDATE achievements SET attempts = '{}' WHERE discipline_name = '{}' and athlete_number = {}".format(attempts, discipline_name, athlete_number)
        elif result[0]: # There are already attempts stored in the DB
            attempts = result[0]
            attempts += '/' + attempt
            query = "UPDATE achievements SET attempts = '{}' WHERE discipline_name = '{}' and athlete_number = {}".format(attempts, discipline_name, athlete_number)
        else: # No attempts stored in DB
            query = "UPDATE achievements SET attempts = '{}' WHERE discipline_name = '{}' and athlete_number = {}".format(attempt, discipline_name, athlete_number)

        if self.DB_Handler.commit_statement(query):
            return 1
        else:
            return 0
        
    def store_result(self, discipline_name, group_name, all_attempts):
        """Store the final version of the achievements in the database

        This is done when the discipline is finished
        1. Validate the stored attempts in the database
        2. get the best attempt for every Athlete
        3. Calculate the Points for every athlete
        4. Store the results in the database
        ...
        Paramters
        ---------
        discipline_name: str
            Name of the Discipline
        group_name: str
            Name of the Group
        attempt_hash: list
            List of Attempt Strings
        """

        if not self._validate_database(discipline_name, group_name, all_attempts):
            print('Stored Attempts do not match sent attempts >>> {}, {}'.format(discipline_name, group_name))
            return 0 

        query = "SELECT athlete_number, attempts, age_group, gender FROM achievements JOIN athletes ON athlete_number = number WHERE discipline_name = '{}' AND achievements.group_name = '{}';".format(discipline_name, group_name)            
        athletes_attempts = self.DB_Handler.get_results(query)
        for athletes_attempt in athletes_attempts:
            athlete_number = athletes_attempt[0]
            attempts = athletes_attempt[1]
            age_group = athletes_attempt[2]
            gender = athletes_attempt[3]
            best_attempt = self._get_best_attempt(discipline_name, attempts)
            if 'U' in age_group:
                points = self.calculator.triathlon[discipline_name](best_attempt, age_group, gender)
            elif age_group == 'U14' or age_group == 'U16':
                points = self.calculator.pentathlon[discipline_name](best_attempt, age_group, gender)
            else:
                points = self.calculator.decathlon[discipline_name](best_attempt, gender)

            query = "UPDATE achievements SET points = {},  best_attempt = {} WHERE athlete_number = {} AND discipline_name = '{}';".format(points, best_attempt, athlete_number, discipline_name)
            if self.DB_Handler.commit_statement(query):
                continue
            else:
                return 0
        return 1

    def _get_best_attempt(self, discipline_name, attempts):
        """Get the best attempt from the Attempts-String
        ...
        Paramters
        ---------
        discipline_name: str
            Name of the Discipline
        attempts: str
            String of all attempts
        
        Return
        -----
        str
            Best attempts
        """

        if len(attempts.split('/')) == 1: # Only 1 attempt --> Run - Discipline
            return attempts

        if discipline_name == 'Hochsprung':
            starting_height = 80
            height_increase = 4
            i = attempts.rfind('O') # index of last successfull jump
            heights = attempts[0:i].count('/') # count heights till this jump
            height = starting_height + height_increase * heights
            return height

        if discipline_name == 'Stabhochsprung':
            starting_height = 120
            height_increase = 20
            i = attempts.rfind('O') # index of last successfull jump
            heights = attempts[0:i].count('/') # count heights till this jump
            height = starting_height + height_increase * heights
            return height
        
        best_attempt = 0
        for attempt in attempts.split('/'):
            if attempt == '-':
                continue
            if float(attempt) > best_attempt:
                best_attempt = float(attempt)

        return best_attempt

    def _validate_database(self, discipline_name, group_name, attempts):
        """Validates the stored Elements in the database

        This is done by comparing the attemps paramters to the string stored in the database
        ...
        Paramters
        ---------
        discipline_name: str
            Name of the Discipline
        group_name: str
            Name of the Group
        attempts: str
            String of all attempts from all Athletes of this group
        """
        query = "SELECT attempts FROM achievements WHERE discipline_name = '{}' AND group_name = '{}'".format(discipline_name, group_name)
        stored_attempts = self.DB_Handler.get_results(query)
        stored_attempts = [ x[0] for x in stored_attempts ]

        if sorted(attempts) == sorted(stored_attempts):
            return 1
        else:
            return 0

    def set_starting_height(self, athlete_number, group_name, discipline_name, height):
        """Set the starting height for 'Hochsprung / Stabhochsprung'

        This is done by storing '-/' attempts in the database for every height till the startin height
        ...
        Paramters
        --------
        athlete_number: int
            Number of the Athlete
        group_name: str
            Name of the group
        discipline_name: str
            Name of the discipline
        height: int
            height in cm
        """

        if discipline_name == 'Hochsprung':
            starting_height = 80
            height_increase = 4
        elif discipline_name == 'Stabhochsprung':
            starting_height = 120
            height_increase = 20

        # count attempts from athlete starting height to general starting height
        heights = int((height - starting_height) / height_increase)
        attempts = ''
        for i in range(heights):
            attempts += '-/'
        
        query = "INSERT INTO achievements (athlete_number, discipline_name, group_name, attempts) VALUES ({}, '{}', '{}', '{}')".format(athlete_number, discipline_name, group_name, attempts)
        if self.DB_Handler.commit_statement(query):
            return 1
        else:
            return 0


class Points_Calculator():
    """Class to Calculate Points
    ...
    Attributes
    ----------
    calculator_decathlon: dict
        Dict with functions to calculate points for every discipline

    calculator_trathlon: dict
        Dict with function to calcualte points for every discipline
    """

    def __init__(self):
        self.decathlon = {
            '100-Meter': self.Points_HundertMeter,
            'Weitsprung': self.Points_Weitsprung,
            'Kugel-Stoßen': self.Points_KugelStossen,
            'Hochsprung': self.Points_Hochsprung,
            '400-Meter': self.Points_VierHundertMeter, 
            '110-Meter-Hürder': self.Points_HunderZehnMeter, 
            'Diskus': self.Points_Diskus, 
            'Stabhochsprung': self.Points_Stabhochsprung, 
            'Speerwurf': self.Points_Speerwurf, 
            '1500-Meter': self.Points_TausendFunfhundertMeter
        }
        
        self.triathlon = {
            '60-Meter': self.Points_sechzigMeter,
            'Weitsprung': self.Points_Weitprung_Kids, 
            'Schlagball': self.Points_Schlagball
        }

        self.pentathlon = {
            '100-Meter': self.Points_HundertMeter_Juveniers,
            'Weitsprung': self.Points_Weitsprung_Juveniers,
            'Hochsprung': self.Points_Hochsprung_Juveniers,
            '60-Meter-Hürdern': self.Points_sechzigMeterHurdle,
            'Crosslauf': self.Points_CrossLauf
        }

    def Points_HundertMeter(self, achievement, gender):
        return 100
    
    def Points_Weitsprung(self, achievement, gender):
        return 100

    def Points_KugelStossen(self, achievement, gender):
        return 100
    
    def Points_Hochsprung(self, achievement, gender):
        return 100

    def Points_VierHundertMeter(self, achievement, gender):
        return 100
    
    def Points_HunderZehnMeter(self, achievement, gender):
        return 100
    
    def Points_Diskus(self, achievement, gender):
        return 100
    
    def Points_Stabhochsprung(self, achievement, gender):
        return 100
    
    def Points_Speerwurf(self, achievement, gender):
        return 100
    
    def Points_TausendFunfhundertMeter(self, achievement, gender):
        return 100

    def Points_sechzigMeter(self, achievement, age_group, gender):
        return 100
    
    def Points_Weitprung_Kids(self, achievement, age_group, gender):
        return 100
    
    def Points_Schlagball(self, achievement, age_group, gender):
        return 100

    def Points_HundertMeter_Juveniers(self, achievement, age_group, gender):
        return 100
    def Points_Weitsprung_Juveniers(self, achievement, age_group, gender):
        return 100
    def Points_Hochsprung_Juveniers(self, achievement, age_group, gender):
        return 100
    def Points_sechzigMeterHurdle(self, achievement, age_group, gender):
        return 100
    def Points_CrossLauf(self, achievement, age_group, gender):
        return 100