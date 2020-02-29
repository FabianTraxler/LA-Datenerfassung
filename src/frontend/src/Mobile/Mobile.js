import React from "react";

import Homescreen from './Modules/Homescreen'
import BeforeDiscipline from './Modules/BeforeDiscipline'
import DisciplineActive from './Modules/DisciplineActive'
import Final from './Modules/Final'
import LoadingScreen from './Modules/LoadingScreen'

import './Mobile.css'


export default class Mobile extends React.Component {
    constructor(props) {
        super(props);
  
        this.state = {
            has_cookie: document.cookie.includes('group'),
            screen_to_show: 'LoadingScreen',
            group: ''
        };

        this.set_screen = this.set_screen.bind(this)
        this.refresh_page = this.refresh_page.bind(this)
      }

      set_screen(){
        if (document.cookie.includes('group')){
            var url = '/group/state/' + document.cookie.split('=')[1]
            fetch(url , {
                headers: {
                    'Content-Type': 'application/json'
                  }
            })
            .then(res => res.json())
            .then((data) => {
                this.setState({screen_to_show: data.response, group:document.cookie.split('=')[1]})
            })
            .catch(console.log)
          }
          else{
              this.setState({screen_to_show: 'homescreen'})
          }
      }

          
      refresh_page(){
            this.set_screen()
        }

      componentDidMount() {
            this.set_screen()
      }



      render (){
          switch(this.state.screen_to_show){

            case 'homescreen':
                return(
                    <Homescreen refresh={this.refresh_page}/>
                )
            
            case 'before_discipline':
                return(
                    <BeforeDiscipline refresh={this.refresh_page} group={this.state.group}/>
                )
            
            case 'discipline_active':
                return(
                    <DisciplineActive refresh={this.refresh_page} group={this.state.group}/>
                )

            case 'final':
                return(
                    <Final refresh={this.refresh_page} group={this.state.group}/>
                )
            
            default:
                return(
                    <LoadingScreen/>
                )
    
          }
         
        }

}