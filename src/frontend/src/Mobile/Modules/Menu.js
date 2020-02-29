import React from "react";
import './Style/Menu.css'
import menu_button from './Style/Image/menu_button.png'
import menu_arrow from './Style/Image/menu_arrow.png'

export default class Menu extends React.Component {
        constructor(props) {
                super(props);
          
                this.state = {
                    menu: 'small',
                    button_style: {
                        backgroundImage: `url(${menu_button})`
                    },
                    menue_items_style: {
                        height: 0
                    }
                };
                this.toggleMenu = this.toggleMenu.bind(this)
                this.handleClick = this.handleClick.bind(this)
              }
            
        toggleMenu(){
            //toggle the Menu from small to big or reverse
            if(this.state.menu === 'small'){
                this.setState({
                    'menu':'big', 
                    'button_style': {backgroundImage: `url(${menu_arrow})`},
                    'menue_items_style': {height: '90vh'}
                })
            }else if(this.state.menu === 'big'){
                this.setState({
                    'menu':'small', 
                    'button_style': {backgroundImage: `url(${menu_button})`},
                    'menue_items_style': {height: '0'}
                })
                document.getElementById('menu_items').style.hegth = 'none'

            }
        }
        
        handleClick(event){
            event.preventDefault()
            switch(event.target.textContent){
                case 'Athletenübersicht':
                    break;
                case 'Regeln':
                    break;
                case 'Zeitplan':
                    break;
                case 'Abmelden':
                    deleteAllCookies()
                    this.props.refresh()
                    break;
                default:
                    console.log('Something went Wrong ... (Menu handleClick)')

            }
        }
        render(){
                return (
                        <div id='menu'>
                                <div id='header'>
                                    <div id='group_title'>{this.props.group}</div>
                                    <div id='toggle_button' onClick={this.toggleMenu} style={this.state.button_style}> </div>
                                </div>
                                <div id='menu_items' style={this.state.menue_items_style}>
                                    <div className='menu_item' onClick={this.handleClick}>Athletenübersicht</div>
                                    <div className='menu_item' onClick={this.handleClick}>Regeln</div>
                                    <div className='menu_item' onClick={this.handleClick}>Zeitplan</div>
                                    <div className='menu_item' onClick={this.handleClick}>Abmelden</div>
                                </div>
                        </div>
                        );
                }
}

function deleteAllCookies() {
    var cookies = document.cookie.split(";");

    for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i];
        var eqPos = cookie.indexOf("=");
        var name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
        document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT";
    }
}