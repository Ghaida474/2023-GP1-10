
import React, {useEffect } from 'react'
import { ChatEngineWrapper, ChatSocket, ChatFeed } from 'react-chat-engine'
import { PrettyChatWindow } from "react-chat-engine-pretty";
import './ChatGroupComponent.css';


const ChatGroupComponent = () => {
    console.log('in ChatGroupComponent');
    useEffect(() => {
      /* eslint-disable no-undef */
      const username = window.username;
      const secret = window.secret;
      const chatgroup_id = window.chatid;
      const access_key = window.access_key
      /* eslint-enable no-undef */
  
      console.log(username);
      console.log(secret);
      console.log(chatgroup_id);
      console.log(access_key);
    }, []); 
  
   return (
        <ChatEngineWrapper>
          <ChatSocket offset={3}
            projectID='f0e1d373-0995-4a51-a2df-cf314fc0e034'
            chatID={window.chatid}
            chatAccessKey={window.access_key}
            senderUsername={window.username}
          />
          <ChatFeed activeChat={window.chatid} /> 
        </ChatEngineWrapper>
    );
}

export default ChatGroupComponent;
