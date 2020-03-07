import React from "react";
import Menu from './Menu'

import './Style/BeforeDiscipline.css'

export default class BeforeDiscipline extends React.Component {
        constructor(props) {
                super(props);
          
                this.state = {
                        completed_disciplines_percent: 0,
                        next_discipline: '',
                        time: '',
                        venue: ''
                }

                this.bewerbStarten = this.bewerbStarten.bind(this)
        }

        componentWillMount(){
                var url = '/group/before_discipline_info/'+ this.props.group
                fetch(url)
                .then(res => res.json())
                .then((data) => {
                    this.setState({
                            'completed_disciplines_percent': data.response.completed_disciplines_percent, 
                            'next_discipline':data.response.next_discipline,
                            'time': data.response.time, 
                            'venue':data.response.venue
                        })
                })
                .catch(console.log)
        }

        bewerbStarten(event){
                event.preventDefault();
                const formData = new FormData();
                formData.append('name', this.props.group)
                formData.append('state', 'discipline_active')
                fetch('/group/state' , {
                        method: 'POST',
                        body:formData
                    })
                    .then(res => res.json())
                    .then((data) => {
                            if(data.response === 'Failed'){
                                    alert('Fehler')
                            }else{
                                this.props.refresh()
                            }
                    })
        }

        render(){
                return (
                        <div>
                                <Menu group={this.props.group} refresh={this.props.refresh}/>
                                <div id='beforeDiscipline_container'>
                                        <div className='fortschritt'>
                                                Fortschritt ...
                                                <div className='fortschritt_container'> <div className='fortschritt_filler' style={{ width : `${this.state.completed_disciplines_percent}%`}}></div>
                                                </div>
                                        </div>
                                        <hr></hr>

                                        <div className='container'>
                                                Nächster Bewerb 
                                                <div className='inner_container next_discipline'>
                                                        {this.state.next_discipline}
                                                </div>
                                        </div>
                                        <div className='container'>
                                                Ort
                                                <div className='inner_container place'>
                                                        {this.state.venue}
                                                </div>
                                        </div>
                                        <div className='container'>
                                                Geplanter Start
                                                <div className='inner_container time'>
                                                        {this.state.time}
                                                </div>
                                        </div>
                                        <div id='start_button' onClick={this.bewerbStarten}>Bewerb starten</div>
                                </div>
                        </div>
                        );
                }
}