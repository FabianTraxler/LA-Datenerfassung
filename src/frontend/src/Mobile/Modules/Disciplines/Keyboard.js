import React from "react";

import './Style/Keyboard.css'

export default class Keyboard extends React.Component {
    constructor(props) {
        super(props);

        this.handleClick = this.handleClick.bind(this)

    }

    handleClick(event){
        event.preventDefault()
        var target = event.target

        if(target.innerHTML === '&lt;--'){
            target.className = 'deleted'
            setTimeout(function(){
                target.className = 'delete'
            }, 100)
            this.props.delete()
        }
        else{
            target.className = 'clicked'
            setTimeout(function(){
                target.className = ''
            }, 100)
            this.props.getNumber(target.innerHTML)
        }

    }


    render(){
        return(
            <div id='Keyboard'>
                <div>
                    <div onClick={this.handleClick}>1</div><div onClick={this.handleClick}>2</div><div onClick={this.handleClick}>3</div>
                </div>
                <div>
                    <div onClick={this.handleClick}>4</div><div onClick={this.handleClick}>5</div><div onClick={this.handleClick}>6</div>
                </div>
                <div>
                    <div onClick={this.handleClick}>7</div><div onClick={this.handleClick}>8</div><div onClick={this.handleClick}>9</div>
                </div>
                <div>
                    <div onClick={this.handleClick}>.</div><div onClick={this.handleClick}>0</div><div onClick={this.handleClick} className='delete'>&lt;--</div>
                </div>
                
            </div>
        )
    }
}
