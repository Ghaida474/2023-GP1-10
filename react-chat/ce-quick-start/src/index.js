
import React from 'react';
import ReactDOM from 'react-dom';
import ChatComponent from './ChatComponent';
import ChatGroupComponent from './ChatGroupComponent';
import reportWebVitals from './reportWebVitals';

const root = document.getElementById('root');
const template = window.template;

if (window.template === 'chat') {
  ReactDOM.createRoot(root).render(<ChatComponent />);
} else if (window.template === 'chatgroup') {
  ReactDOM.createRoot(root).render(<ChatGroupComponent />);
}

reportWebVitals();

