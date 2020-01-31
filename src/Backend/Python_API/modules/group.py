from collections import defaultdict 


class Group_Handler():
    def __init__(self, DB_Handler):
        self.DB_Handler = DB_Handler
        self.group_disciplines = {
            "Decathlon": ['100 Meter', 'Weitsprung', 'Kugel Stoßen', 'Hochsprung', '400 Meter', '110 Meter', 'Diskus', 'Stabhochsprung', 'Speerwurf', '1500 Meter'],
            "Pethathlon": ['100 Meter', 'Weitsprung', 'Hochsprung', 'Speerwurf', '1200 Meter'],
            "Triathlon": ['60 Meter', 'Weitsprung', 'Schlagball']
        }

    def get_available_groups(self):
        """"Returns Dict with Categories as keys and list of Groups as values"""

        query = 'SELECT name, category FROM Groups;'
        rows = self.DB_Handler.get_results(query)
        result = defaultdict(list)
        for row in rows:
            result[row[1]].append(row[0])
        return result

    def get_disciplines(self, group_name):
        """Returns List of all Disciplines for a given Group"""

        query = 'SELECT type FROM Groups WHERE name = {}'.format(group_name)
        row = self.DB_Handler.get_result(query)
        type_ = row[0]
        return self.group_disciplines[type_]

    def get_athletes(self, group_name):
        """Returns List of all Athletes for a given Group"""

        query = 'SELECT number, first_name, last_name FROM Athletes WHERE group_name = {}'.format(group_name)
        rows = self.DB_Handler.get_results(query)
        athletes = {}
        for row in rows:
            athletes[row[0]] = {}
            athletes[row[0]]['Vorname'] = row[1]
            athletes[row[0]]['Nachname'] = row[2]
            athletes[row[0]]['Punkte'] = 0
        
        query = 'SELECT athlete_number, points FROM Achievements WHERE group_name = {}'.format(group_name)
        rows = self.DB_Handler.get_results(query)
        for row in rows:
            athletes[row[0]]['Punkte'] += int(row[1])

        return athletes

    def get_score(self, group_name):
        
        return

    def create(self, group_name, type):
        return 'Group Created'

    def create_password(self, group_name):
        return

    def get_status(self, group_name):
        return

