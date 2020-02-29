class Event_Handler():
    """Database Interface for all event specific agendas
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

    def store_event(self, group_name, discipline_name, starting_time, venue):
        """Create a new Event
        ...
        Parameters
        ----------
        group_name: str
            Name of the Group
        
        discipline_name: str
            Name of the discipline
        
        starting_time: str
            String representation of the starting time (eg. '11:30')

        venue: str
            Name of the Venue (eg. 'Weitprung 1)
        """
        query = "INSERT INTO events VALUES ('{}','{}','{}','{}');".format(group_name, discipline_name, starting_time, venue)
        if self.DB_Handler.commit_statement(query):
            return 1
        else:
            return 0

    def update_event(self, group_name, discipline_name, column, new_value):
        """Create a new Event
        ...
        Parameters
        ----------
        group_name: str
            Name of the Group
        
        discipline_name: str
            Name of the discipline
        
        column: str
            Columns which should be updated

        new_value: str
            New Value to be inserted
        """
        query = "UPDATE events SET {} = '{}' WHERE group_name = '{}' AND discipline_name = '{}'".format(column, new_value, group_name, discipline_name)
        if self.DB_Handler.commit_statement(query):
            return 1
        else:
            return 0

    def get_time_and_venue(self, group_name, discipline_name):
        """ Get time and venue of an event
        ...
        Paramters
        ---------
        group_name: str
            Name of the Group
        
        discipline_name: str
            Name of the discipline

        Return
        ------
        tuple:
            Tuple of time and venue as strings
        """
        query = "SELECT starting_time, venue FROM events WHERE group_name = '{}' and discipline_name = '{}'".format(group_name, discipline_name)
        row = self.DB_Handler.get_result(query)
        return row