import React from "react";

import './Style/DisciplineOneAttempt.css'

export default class DisciplineOneAttempt extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
                discipline: this.props.discipline
        };
        this.fillLaufContainer = this.fillLaufContainer.bind(this)
    }

    fillLaufContainer(){
        let laufe_divs = []

        this.state.discipline.laufeinteilung.laufe.forEach(lauf => {
            laufe_divs.push(this.createLauf(lauf, this.state.discipline.laufeinteilung[lauf]))
        });

        return(
            <div className='laufe_container'>
                {laufe_divs}
            </div>
        )
    }

    createLauf(lauf, bahnen){
        let bahnen_div = []
        Object.keys(bahnen).forEach( bahn => {
            bahnen_div.push(
                <div className='bahn_container' key={bahn}>
                    <div className='bahn_number'>{bahn.split(' ')[1]}</div>
                    <div className='athlete_name'>{bahnen[bahn][1]}</div>
                    <div className='athlete_number'>{bahnen[bahn][0]}</div>
                    <div className='athlete_performance'>{bahnen[bahn][2]}</div>
                </div>
            )
        })
        return (
            <div className='lauf_container' key={lauf}>
                <div className='lauf_number' onClick={this.expandLauf}>{lauf}</div>
                <div className='lauf_info' id={lauf}>
                    <div className='lauf_header'>
                        <div className='bahn_number'>Bahn</div>
                        <div className='athlete_name'>Name</div>
                        <div className='athlete_number'>#</div>
                        <div className='athlete_performance'>Zeit</div>
                    </div>
                    {bahnen_div}
                   <div id='lauf_gestartet' onClick={this.laufGestartet}>Lauf gestartet</div>
                </div>
            </div>
        )
    }

    laufGestartet(event){
        document.getElementById(event.target.parentNode.id).classList.toggle('lauf_info_active')
        let lauf_nr = parseInt(event.target.parentNode.id.split(' ')[1]) + 1
        if(document.getElementById('Lauf ' + lauf_nr) !== null){
            document.getElementById('Lauf ' + lauf_nr).classList.toggle('lauf_info_active')
        }else{
            document.getElementById('discipline_finished').classList.add('discipline_finished_active')
        }
    }

    expandLauf(event){
        var laufe = document.getElementsByClassName('lauf_info')
        for(var i = 0; i<laufe.length;i++){
            if(laufe[i].id !== event.target.innerHTML){
                laufe[i].classList.remove('lauf_info_active')
            }
        }
        document.getElementById(event.target.innerHTML).classList.toggle('lauf_info_active')
    }

    componentDidMount(){
        document.getElementById('Lauf 1').classList.add('lauf_info_active')
    }
    finish_discipline(){
        this.state.discipline.finish_discipline(this.props.refresh)
    }

    render(){
        return(
            <div id='oneAttempt_container'>
                <div id='discipline_finished' className='discipline_finished'>
                    Bewerb <br></br> abgeschlossen
                    <div onClick={this.finish_discipline} > Ergebnis speichern </div>
                </div>
                {this.fillLaufContainer()}
                <div id='finish_button'></div>
            </div>
        )
    }
}
