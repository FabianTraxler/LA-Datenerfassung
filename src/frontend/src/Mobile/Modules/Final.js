import React from "react";
import Menu from './Menu'

import './Style/Final.css'

export default class Final extends React.Component {
        constructor(props) {
                super(props);
          
                this.state = {
                        button_style:{
                                display:'block'
                        }
                };
                this.handleClick = this.handleClick.bind(this)
              }
        
        handleClick(event){
                event.preventDefault()
                this.setState({
                        'button_style':{
                                display:'none'
                        }
                })
                alert('Urkunden ausgedruckt')
        }
        
        render(){
                return (
                        <div>
                                <Menu group={this.props.group} refresh={this.props.refresh} />
                                <div id='final_container'>
                                        <div id='image'></div>
                                        <h1>Alle Bewerbe abgeschlossen</h1>
                                        <button onClick={this.handleClick} style={this.state.button_style}>Urkunden ausdrucken</button>
                                </div>
                        </div>
                        );
                }
}