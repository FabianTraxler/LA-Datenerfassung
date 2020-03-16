import React from "react";

class Athlete{
    constructor(number, first_name, last_name, attempts_string){
        this.number = number
        this.first_name = first_name
        this.last_name = last_name
        this.name = first_name + ' ' + last_name
        this.attempts_string = attempts_string

        this.nr_attempts = 0
        if (attempts_string){
            this.nr_attempts = attempts_string.split('/').length
        }       
    }

    save_attempt(group_name, discipline_name, attempt){
        // Save to Database
        if (this.attempts_string){
            this.attempts_string += '/' + attempt
        }else{
            this.attempts_string = attempt
        }
        

        const formData = new FormData();
        formData.append('athlete_number', this.number)
        formData.append('group_name', group_name)
        formData.append('discipline_name', discipline_name)
        formData.append('attempt', attempt)

        
        fetch('/attempt' , {
            method: 'POST',
            body:formData
        })
        .then(res => res.json())
        .then((data) => {
                if(data.response === 'Failed'){
                    alert('Fehler beim Speichern')
                }
        })
    }

    prepare_attempts_div(){
        let attempts = []
        let attempt_classes = []
        for(let i = 0; i < 3; i++){
            let attempt = this.attempts_string.split('/')[i]
            if(attempt === '-'){
                attempts.push('Fehler')
                attempt_classes.push('attempt attempt_fail')
            }else if(attempt){
                attempts.push(attempt + ' Meter')
                attempt_classes.push('attempt attempt_success')
            }else{
                attempts.push('')
                attempt_classes.push('attempt no_attempt')
            }
        }
        return (
            <div id='attempt_container'>
                <div className={attempt_classes[0]}>
                    {attempts[0]}
                </div>
                <div className={attempt_classes[1]}>
                    {attempts[1]}
                </div>
                <div className={attempt_classes[2]}>
                    {attempts[2]}
                </div>
            </div>
        )
    }
}

class Discipline_three_attempts{
    constructor(startreihenfolge_array, name, group_name){
        this.athletes = []
        startreihenfolge_array.forEach(athlete =>{
            this.athletes.push(new Athlete(athlete[0], athlete[1], athlete[2], athlete[3]))
        })

        this.round = this.athletes[0].nr_attempts
        this.athletes_in_preperation_this_round = []
        
        if(this.round === 0){
            this.next_round()
        }else{
            this.get_athletes_in_this_round()
        }

        this.active_athlete_id = this.athletes_in_preperation_this_round.pop()
        this.active_athlete = this.athletes[this.active_athlete_id]

        this.next_athlete_id = this.athletes_in_preperation_this_round[this.athletes_in_preperation_this_round.length - 1]       
        this.next_athlete = this.athletes[this.next_athlete_id]
 
        if(!this.next_athlete_id){
            this.next_athlete_id = 0
            this.next_athlete = this.athletes[this.next_athlete_id]
            if(this.round === 3){
                this.next_athlete =  new Athlete('', 'Bewerb', 'Ende', '') 
            }
        }

        this.name = name

        this.group_name = group_name

        this.state = 'inProgress'
        if (this.round >= 4){
            this.state = 'Finished'
        }
    }

    next_round(){

        this.round += 1

        if (this.round >= 4){
            this.state = 'Finished'
        }
        this.get_athletes_in_this_round()
        
    }

    get_athletes_in_this_round(){
        this.athletes_in_preperation_this_round = []
        this.athletes.forEach(athlete => {
            if(athlete.nr_attempts < this.round){
                this.athletes_in_preperation_this_round.push(this.athletes.indexOf(athlete))
            }
        })
        if(this.athletes_in_preperation_this_round.length === 0){
            this.next_round()
        }else{
            this.athletes_in_preperation_this_round.reverse()
        }
    }

    save_attempt(attempt){
        this.active_athlete.save_attempt(this.group_name, this.name, attempt)
        if(this.athletes_in_preperation_this_round.length > 1){
            this.active_athlete_id = this.athletes_in_preperation_this_round.pop()
            this.active_athlete = this.athletes[this.active_athlete_id]

            this.next_athlete_id = this.athletes_in_preperation_this_round[this.athletes_in_preperation_this_round.length - 1]        
            this.next_athlete = this.athletes[this.next_athlete_id]
        }else if(this.athletes_in_preperation_this_round.length === 1){
            this.active_athlete_id = this.athletes_in_preperation_this_round.pop()
            this.active_athlete = this.athletes[this.active_athlete_id]
            if (this.round === 3){
                this.next_athlete_id = 0
                this.next_athlete = new Athlete('', 'Bewerb', 'Ende', '')
            }else{
                this.next_athlete_id = 0
                this.next_athlete = this.athletes[this.next_athlete_id]
            }
        }else if(this.athletes_in_preperation_this_round.length === 0){
            this.next_round()

            this.active_athlete_id = this.athletes_in_preperation_this_round.pop()
            this.active_athlete = this.athletes[this.active_athlete_id]

            this.next_athlete_id = this.athletes_in_preperation_this_round[this.athletes_in_preperation_this_round.length - 1]        
            this.next_athlete = this.athletes[this.next_athlete_id]
        }
    }

    finish_discipline(refresh){
        let all_attempts = []
        this.athletes.forEach(athlete =>{
            all_attempts.push(athlete.attempts_string)
        })
        let formData = new FormData()
        formData.append('group_name', this.group_name)
        formData.append('discipline_name', this.name)
        formData.append('attempts', all_attempts)

        fetch('/group/discipline_completed' , {
            method: 'POST',
            body:formData
        })
        .then(res => res.json())
        .then((data) => {
                if(data.response === 'Failed'){
                    alert('Fehler beim Speichern')
                }else{
                    fetch('/result' , {
                        method: 'POST',
                        body:formData
                    })
                    .then(res => res.json())
                    .then((data) => {
                            if(data.response === 'Failed'){
                                alert('Fehler beim Speichern')
                            }else{
                                refresh()
                            }
                    })
                }
        })
    }
}

class Discipline_one_attempt{
    constructor(startreihenfolge_array, name, group_name){
        this.laufeinteilung = {}
        this.laufeinteilung.laufe = []
        startreihenfolge_array.forEach(athlete =>{
            let lauf = 'Lauf ' + athlete[4].split('_')[0]
            let bahn = 'Bahn ' + athlete[4].split('_')[1]
            if(!this.laufeinteilung[lauf]){
                this.laufeinteilung.laufe.push(lauf)
                this.laufeinteilung[lauf] = {}
            }
            this.laufeinteilung[lauf][bahn] = [athlete[0], athlete[1] + ' ' + athlete[2], athlete[3]] // [ Nummer , Name , Ergebnis ]
        })

        this.name = name

        this.group_name = group_name
    }

    finish_discipline(refresh){
        let formData = new FormData()
        formData.append('group_name', this.group_name)
        formData.append('discipline_name', this.name)

        fetch('/group/discipline_completed' , {
            method: 'POST',
            body:formData
        })
        .then(res => res.json())
        .then((data) => {
                if(data.response === 'Failed'){
                    alert('Fehler beim Speichern')
                }else{
                    refresh()
                }
        })
    }


}


class Discipline_three_plus_attempts{
    constructor(startreihenfolge_array, name, group_name){

    }
}

export default function createDiscipline(discipline_typ, startreihenfolge_array, name, group_name){
    if(discipline_typ === 'one_attempt'){
        return new Discipline_one_attempt(startreihenfolge_array, name, group_name)
    }else if (discipline_typ === 'three_attempts'){
        return new Discipline_three_attempts(startreihenfolge_array, name, group_name)
    }else if (discipline_typ === 'three_plus_attempts'){
        return new Discipline_three_plus_attempts(startreihenfolge_array, name, group_name)
    }
}