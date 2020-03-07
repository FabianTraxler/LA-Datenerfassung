from collections import defaultdict 
import hashlib

class Group_Handler():
    """Database Interface for all group specific agendas
    ...
    Attributes
    ----------
    DB_Handler: DB_Handler
        An Object wto interact with the database

    group_disciplines_order: dict
        shows the disciplines of the different event formats
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
            "Decathlon_Normal": ['100-Meter', 'Weitsprung', 'Kugel-Stoßen', 'Hochsprung', '400-Meter', '110-Meter-Hürden', 'Diskus', 'Stabhochsprung', 'Speerwurf', '1500-Meter'],
            "Decathlon_Odd": ['100-Meter', 'Diskus', 'Stabhochsprung', 'Speerwurf',  '400-Meter', '110-Meter-Hürden', 'Weitsprung', 'Kugel-Stoßen', 'Hochsprung', '1500-Meter'],
            "Pethathlon_Normal": ['100-Meter', 'Weitsprung', 'Hochsprung', 'Speerwurf', '1200-Meter'],
            "Triathlon_Normal": ['60-Meter', 'Weitsprung', 'Schlagball']
        }


    def get_available_groups(self):
        """"Returns Dict with Categories as keys and list of Groups as values"""

        query = 'SELECT name, type FROM groups;'
        rows = self.DB_Handler.get_results(query)
        result = defaultdict(list)
        for row in rows:
            result[row[1]].append(row[0])
        return result

    def get_disciplines(self, group_name):
        """Returns List of all Disciplines for a given Group
                ...
        Paramters
        --------
        group_name: str
            Name of the Group
        
        Returns
        -------
        list
            List of Discipline Names
        """

        query = "SELECT type, discipline_order FROM groups WHERE name = '{}'".format(group_name)
        row = self.DB_Handler.get_result(query)
        typ, discipline_order = row
        return self.group_disciplines_order[typ + '_' + discipline_order]

    def get_athletes_starting_order(self, group_name, discipline_name):
        """Get the starting order of the athletes (sorted by number)
        ...
        Parameters
        ---------
        group_name: str
            Name of the group

        Returns
        -------
        list
            ordered list of Tuples 
            [(Number, First-Name, Family-Name), ...]
        """

        query = "Select number, first_name, last_name, attempts, lauf_bahn FROM athletes JOIN achievements ON number = athlete_number WHERE athletes.group_name = '{}' AND discipline_name = '{}';".format(group_name, discipline_name)
        rows = self.DB_Handler.get_results(query)
        return sorted(rows)

    def get_athletes_overall_points(self, group_name):
        """ Get the Overall points of all Athletes of a group
        ...
        Paramters
        --------
        group_name: str
            Name of the Group
        
        Returns
        -------
        list
            List of Tuples of all Athletes for a given Group 
            [(Athlete_Number, Name, Family_Name, Overall_Points)]
        
        """

        query = "SELECT number, first_name, last_name FROM athletes WHERE group_name = '{}';".format(group_name)
        rows = self.DB_Handler.get_results(query)
        athletes = {}
        for row in rows:
            athletes[row[0]] = {}
            athletes[row[0]]['Vorname'] = row[1]
            athletes[row[0]]['Nachname'] = row[2]
            athletes[row[0]]['Punkte'] = 0
        
        query = "SELECT athlete_number, points FROM achievements WHERE group_name = '{}';".format(group_name)
        rows = self.DB_Handler.get_results(query)
        for row in rows:
            athletes[row[0]]['Punkte'] += int(row[1])
        
        result = []
        for key, item in athletes.items():
            result.append((key, item['Vorname'], item['Nachname'], item['Punkte']))

        return sorted(result)

    def get_athletes_discpline_performance(self, group_name, discipline_name):
        """Get the performance of all athletes of a group in a discipline
        ...
        Paramters
        ---------
        group_name: str
            Name of the Group

        discipline_name: str
            Name of the Discpiline

        Returns
        -------
        list
            List of Tuples of all Athletes for a given Group 
            [(Athlete_Number, Name, Family_Name, Performance)]
        """

        query = "SELECT number, first_name, last_name, best_attempt FROM athletes INNER JOIN achievements on number = athlete_number WHERE athletes.group_name = '{}' and discipline_name = '{}' ;".format(group_name, discipline_name)
        result = self.DB_Handler.get_results(query)

        return sorted(result)

    def get_next_discipline(self, group_name):
        """Get the next/currently active disciline for a given group
        ...
        Paramters
        ---------
        group_name: str
            Name of the Group
        
        Returns
        -------
        string
            Name of the next/currently active discipline
        """

        query = "SELECT type, discipline_order, completed_disciplines FROM groups WHERE name = '{}'".format(group_name)
        row = self.DB_Handler.get_result(query)
        typ, discipline_order, completed_disciplines = row
        completed_disciplines_percent = (completed_disciplines / len(self.group_disciplines_order[typ + '_'+ discipline_order])) * 100
        next_discipline = self.group_disciplines_order[typ + '_' + discipline_order][completed_disciplines]
        return completed_disciplines_percent, next_discipline

    def discpline_completed(self, group_name, discipline_name, attempts):
        """Compare if stored achiements in Database match the sent achiements and then mark the discipline as complete
        ...
         Parameters
        ----------
        group_name: str
            Name of the Group
        
        discipline_name: str
            Name of the finisched Disipline
        
        achievements_hash: str
            all achiements of the atheletes in this discipline  hashed
        """
        query = "SELECT attempts, completed_disciplines, type, discipline_order FROM achievements JOIN groups ON group_name = name  WHERE group_name = '{}' AND discipline_name = '{}';".format(group_name, discipline_name)
        rows = self.DB_Handler.get_results(query)
        stored_attempts = [ x[0] for x in rows ]
        completed_disciplines = rows[0][1]
        total_nr_disciplines = len(self.group_disciplines_order[rows[0][2] + '_' + rows[0][3]])
        if sorted(stored_attempts) == sorted(attempts):
            completed_disciplines += 1
            query = "UPDATE groups SET completed_disciplines = completed_disciplines + 1 WHERE name = '{}';".format(group_name)
            if completed_disciplines == total_nr_disciplines:
                state = 'final'
            else:
                state = 'before_discipline'
            if self.DB_Handler.commit_statement(query) and self.set_state(group_name, state):
                return 1
            else:
                print('Not Stored')
                return 0
        else:
            print("stored and transmitted attempts don't match")
            return 0

    def get_state(self, group_name):
        """Return the current state of the group"""

        query = "SELECT state FROM groups WHERE name = '{}';".format(group_name)
        row = self.DB_Handler.get_result(query)
        return row[0]

    def set_state(self, group_name, state):
        """Set the state of the group"""

        query = "UPDATE groups SET state = '{}' WHERE name = '{}';".format(state, group_name)
        if self.DB_Handler.commit_statement(query):
            return 1
        else:
            return 0
        
    def create_group(self, group_name, typ, discipline_order, supervisor, volunteers, password):
        """Create a new Group
        ...
        Parameters
        ----------
        group_name: str
            Name of the Group
        
        typ: str
            Type of the Group (Decathlon, Triathlon, Pentathlon)
        
        discipline_order: str ("Normal"/"Odd")
            Indicates if the order of the diciplines is normal or odd 
        
        supervisor: str
            Name of the Supervisior of the Group
        
        volunteers: str
            Names of the Volunteers of the Group

        password: str
            Password of the Group
        """
        state = "before_discipline"
        password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()

        query = "INSERT INTO groups VALUES ('{}','{}','{}','{}','{}','{}','{}', '{}');".format(group_name, typ, discipline_order, state, 0,  supervisor, volunteers, password_hash)
        if self.DB_Handler.commit_statement(query):
            return 1
        else:
            return 0

    def get_group_from_password(self, password):
        """ Get the Group which Matched the Password provided
        ...
        Paramters
        --------
        password:str
            Password as String
        Return
        -------
        Return the name of the Group or 'no_group'
        """
        password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
        query = "SELECT name FROM groups WHERE password_hash = '{}';".format(password_hash)
        row = self.DB_Handler.get_result(query)
        if row:
            return row[0]
        else:
            return 'no_group'

    def get_discipline_typ(self, discipline_name):
        """Get the typ of the discipline 
        ...
        Paramters
        --------
        discipline_name: str
            Name of the Discipline
        
        Return
        ------
        str
            Typ of the discipline ("one_attempt", "three_attempts", "threePlus_attempts")
        """

        if discipline_name in ['100-Meter', '400-Meter', '110-Meter-Hürden', '1500-Meter', '60-Meter', '1200-Meter', ]:
            return 'one_attempt'
        
        elif discipline_name in ['Weitsprung', 'Kugel-Stoßen', 'Diskus', 'Speerwurf', 'Schlagball']:
            return 'three_attempts'

        elif discipline_name in ['Hochsprung', 'Stabhochsprung']:
            return 'threePlus_attempts'