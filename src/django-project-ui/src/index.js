import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import 'bootstrap/dist/css/bootstrap.css';
import App from './App';

// import registerServiceWorker from './registerServiceWorker';

let myComponent =  document.getElementById('django-project-django-ui')
if (myComponent !== null){
    ReactDOM.render(<App />,myComponent);
}
