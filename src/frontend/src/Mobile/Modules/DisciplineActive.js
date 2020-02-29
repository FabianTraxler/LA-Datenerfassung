import React from "react";
import Menu from './Menu'
import LoadingScreen from './LoadingScreen'
import DisciplineOneAttempt from './Disciplines/DisciplineOneAttempt'
import DisciplineThreeAttempts from './Disciplines/DisciplineThreeAttempts'
import DisciplineThreePlusAttempts from './Disciplines/DisciplineThreePlusAttempts'

import createDiscipline from './Helper/Discipline'

import './Style/DisciplineActive.css'


export default class DisciplineActive extends React.Component {
        constructor(props) {
                super(props);
          
                this.state = {
                        discipline_typ: '',
                        discipline: ''
                };
              }
        componentWillMount(){
                var url = '/group/discipline_active_info/'+ this.props.group
                fetch(url)
                .then(res => res.json())
                .then((data) => {
                    this.setState({
                            'discipline_typ':data.response.discipline_typ,
                            'discipline':createDiscipline(
                                data.response.discipline_typ,
                                data.response.startreihenfolge, 
                                data.response.active_discipline, 
                                this.props.group)                      
                                })
                })
                .catch(console.log)
        }

        render(){
                switch(this.state.discipline_typ){
                        case 'one_attempt':
                                return (
                                        <div>
                                                <Menu group={this.props.group} refresh={this.props.refresh}/>
                                                <div id='DisciplineActive_container'>
                                                        <DisciplineOneAttempt discipline={this.state.discipline} refresh={this.props.refresh}/>
                                                </div>
                                        </div>
                                );
                        case 'three_attempts':
                                return (
                                        <div>
                                                <Menu group={this.props.group} refresh={this.props.refresh}/>
                                                <div id='DisciplineActive_container'>
                                                        <DisciplineThreeAttempts discipline={this.state.discipline} refresh={this.props.refresh}/>
                                                </div>
                                        </div>
                                );
                        case 'threePlus_attempts':
                                return (
                                        <div>
                                                <Menu group={this.props.group} refresh={this.props.refresh}/>
                                                <div id='DisciplineActive_container'>
                                                        <DisciplineThreePlusAttempts discipline={this.state.discipline} refresh={this.props.refresh}/>
                                                </div>
                                        </div>
                                );
                        default:
                                return(
                                        <div>
                                                <Menu group={this.props.group} refresh={this.props.refresh}/>
                                                <div id='DisciplineActive_container'>
                                                        <LoadingScreen />
                                                </div>
                                        </div>
                                )
                }
                }
}