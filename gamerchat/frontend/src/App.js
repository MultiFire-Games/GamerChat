import React, { useState, useEffect } from 'react';
import Chat from './Chat';
import Voice from './Voice';

function App() {
  const [nick, setNick] = useState('');
  const [connected, setConnected] = useState(false);
  const [ws, setWs] = useState(null);
  const [messages, setMessages] = useState([]);
  const [users, setUsers] = useState([]);

  const connect = () => {
    const socket = new WebSocket('ws://localhost:8000/rtc');

    socket.onopen = () => {
      socket.send(JSON.stringify({ type: 'join', nick }));
      setConnected(true);
    };

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'chat_message') {
        setMessages((prev) => [...prev, `${data.nick}: ${data.message}`]);
      } else if (data.type === 'user_list') {
        setUsers(data.users);
      }
    };

    socket.onclose = () => {
      setConnected(false);
    };

    setWs(socket);
  };

  const sendMessage = (message) => {
    ws.send(JSON.stringify({ type: 'chat_message', nick, content: message }));
  };

  return (
    <div>
      {!connected ? (
        <div>
          <input
            type="text"
            value={nick}
            onChange={(e) => setNick(e.target.value)}
            placeholder="Enter your nickname"
          />
          <button onClick={connect}>Join Chat</button>
        </div>
      ) : (
        <>
          <h3>Users in the chat:</h3>
          <ul>
            {users.map((user, index) => (
              <li key={index}>{user}</li>
            ))}
          </ul>
          <Chat messages={messages} sendMessage={sendMessage} />
          <Voice />
        </>
      )}
    </div>
  );
}

export default App;
