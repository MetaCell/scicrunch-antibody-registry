import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import TagManager from 'react-gtm-module'


const gtmId = "G-T5N7J7V9CN";

if(gtmId) {
  TagManager.initialize({ gtmId })
}




ReactDOM.render(<App />, document.getElementById('root'));
