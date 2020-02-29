import React from "react";
import {
  BrowserRouter as Router,
  Route, 
  Switch,
  useHistory
} from "react-router-dom";
import { isMobile } from 'react-device-detect';
import Mobile from './Mobile/Mobile';
import Desktop from './Desktop/Desktop';

import './App.css'


export default function App() {
  
  return (
    <Router>
      <Switch>
              <Route exact path="/mobile" component={Mobile}/>
              <Route exact path="/desktop" component={Desktop}/>
              <Route component={NotFound}/>
      </Switch>
    </Router>
  );
}

function NotFound(){
  const history = useHistory();

  function mobile() {
    history.push("/mobile");
  }

  if(isMobile) {
    mobile()
  }

  return (
    <div>
      Bitte wenden Sie sich an den Administrator für den richtigen Zugang
    </div>
  )
}