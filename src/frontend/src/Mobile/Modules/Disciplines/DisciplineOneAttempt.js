import React from "react";

export default class DisciplineOneAttempt extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
                discipline: this.props.discipline
        };
    }

    componentDidMount(){
        //document.getElementById
    }


    render(){
        return(
            <div id='oneAttempt_container'>
                <div id='lauf_container'>
                    <div id='header_lauf'>
                        <div>Bahn</div>
                        <div>Nummer</div>
                        <div>Name</div>
                    </div>

                </div>
                <div id='finish_button'></div>
            </div>
        )
    }
}
