import React, {useEffect } from 'react'
import { PrettyChatWindow } from "react-chat-engine-pretty";
import { ChatEngineWrapper, ChatSocket, ChatFeed } from 'react-chat-engine'
import './ChatComponent.css';


const ChatComponent = () => {
  console.log('in ChatComponent');
  useEffect(() => {
    /* eslint-disable no-undef */
    const username = window.username;
    const secret = window.secret;
    /* eslint-enable no-undef */

    console.log(username);
    console.log(secret);
  }, []); 

    return (
      
      <div style={{ height: '100vh', width: '100vw'}}>
          <PrettyChatWindow  offset={3} 
            height='100vh'
            width='50vh'
            username={window.username}
            secret={window.secret}
            projectId='f0e1d373-0995-4a51-a2df-cf314fc0e034'
            style={{ height: '100%'}}
          />
      </div>
    );
}

export default ChatComponent;
