import React from 'react';
import ReactDOM from 'react-dom';
import GappersList from './GappersList'

//import { Provider } from 'react-redux'
//import store from './store'


class Gappers extends React.Component {

  render(){
    return(<React.Fragment>
              <GappersList />
            </React.Fragment>
    )
  }
}

export default Gappers;
