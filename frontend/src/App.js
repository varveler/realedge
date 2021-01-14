import React, {Fragment} from 'react';
import './App.css';
import SearchForm from './components/SearchForm.js'
import ScanButton from './components/ScanButton.js'

function App() {
  return (
    <Fragment>
      <SearchForm/>
      <ScanButton/>
    </Fragment>
  );
}

export default App;
