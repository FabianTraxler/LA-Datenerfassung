import React from "react";

import './Style/Homescreen.css'

export default class Homescreen extends React.Component {
        constructor(props) {
                super(props);
                this.state = {code: ''};

                this.handleChange = this.handleChange.bind(this);
                this.handleSubmit = this.handleSubmit.bind(this);
        }

        storeGroupCookie(group_name){
                var date = new Date()
                date.setTime(date.getTime() + 4*24*60*60*1000);
                document.cookie = 'group=' + group_name  + ';expires=' + date.toGMTString();
        }


        handleChange(event) {
                this.setState({code: event.target.value});
        }
            
        handleSubmit(event) {
                event.preventDefault();
                const formData = new FormData();
                formData.append('password', this.state.code)
                fetch('/group' , {
                        method: 'PUT',
                        body:formData
                    })
                    .then(res => res.json())
                    .then((data) => {
                            if(data.response === 'no_group'){
                                    alert('Falsches Passwort')
                            }else{
                                this.storeGroupCookie(data.response)
                                this.props.refresh()
                            }
                    })
        
                }

        render(){
                return (
                        <div id='Homescreen'>
                                <div id='image'></div>
                                <h1>Gruppen Code eingeben</h1>
                                <form onSubmit={this.handleSubmit}>
                                        <input value={this.state.code} placeholder='Code' type='text' onChange={this.handleChange}></input>
                                        <button type="submit" value='Senden'>Senden</button>
                                </form>
                                
                                <p>Code findet sich am Informationsblatt oder kann im Office erfragt werden</p>
                        </div>
                        );
        }
}