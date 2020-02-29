import React from "react";

import Keyboard from './Keyboard'

import './Style/DisciplineThreeAttempts.css'

export default class DisciplineThreeAttempts extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            discipline: this.props.discipline,
            current_result: '',
        };

        this.getNumber = this.getNumber.bind(this)
        this.saveResult = this.saveResult.bind(this)
        this.delete = this.delete.bind(this)
        this.finish_discipline = this.finish_discipline.bind(this)
    }

    getNumber(number_str){
        this.setState({'current_result': this.state.current_result + number_str })
    }

    delete(){
        this.setState({'current_result': this.state.current_result.substring(0,this.state.current_result.length - 1)})
    }
    saveResult(event){
        event.preventDefault()
        let target = event.target
        target.className = 'save_button saved'
            setTimeout(function(){
                target.className = 'save_button'
            }, 250)

        this.state.discipline.save_attempt(this.state.current_result)
        document.getElementById('versuche_active_athlete').innerHTML += '- ' + this.state.current_result + ' Meter'
        setTimeout(() => {
            this.setState({'current_result': ''})
        }, 500);
    }

    finish_discipline(){
        this.state.discipline.finish_discipline(this.props.refresh)
    }


    componentDidUpdate(){
        if(this.state.discipline.state === 'Finished'){
            document.getElementById('discipline_finished').classList.add('discipline_finished_active')
        }
    }
    componentDidMount(){
        if(this.state.discipline.state === 'Finished'){
            document.getElementById('discipline_finished').classList.add('discipline_finished_active')
        }
    }

    render(){
        return(
            <div>
                <div id='discipline_finished' className='discipline_finished'>
                    Discipline abgeschlossen
                    <div onClick={this.finish_discipline}> Abschließen </div>
                </div>
                <div id='athletes_container'>
                    <div id='athlete_header'>
                        <div className='nummer_column'>#</div>
                        <div className='name_column'>Name</div>
                        <div className='versuche_column'>Versuche</div>
                    </div>
                    <div className='inbetween_text'>In Vorbereitung ...</div>
                    <div id='next_athlete'>
                        <div className='nummer_column'>{this.state.discipline.next_athlete.number}</div>
                        <div className='name_column'>{this.state.discipline.next_athlete.name}</div>
                        <div className='versuche_column'>{this.state.discipline.next_athlete.prepare_attempts_string()}</div>
                    </div>
                    <div className='inbetween_text'>Am Start ...</div>
                    <div id='active_athlete'>
                    <div className='nummer_column'>{this.state.discipline.active_athlete.number}</div>
                        <div className='name_column'>{this.state.discipline.active_athlete.name}</div>
                        <div id='versuche_active_athlete' className='versuche_column'>{this.state.discipline.active_athlete.prepare_attempts_string()}</div>
                    </div>
                </div>
                <div id='result_container'>
                    <div id='result' >{this.state.current_result}</div>
                    <div className='save_button' onClick={this.saveResult}>Speichern</div>
                </div>
                <Keyboard saveResult={this.saveResult} getNumber={this.getNumber} delete={this.delete}/>
            </div>
        )
    }
}
