import React from "react";

export default class DisciplineThreePlusAttempts extends React.Component {
    constructor(props) {
        super(props);
  
        this.state = {
                startreihenfolge: this.props.startreihenfolge
        };
    }


    render(){
        return(
            <div>
                {this.props.active_discipline}
            </div>
        )
    }
}
