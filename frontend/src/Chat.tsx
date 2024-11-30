import {
    Button,
    Card,
    CardBody,
    Col,
    Form,
    FormGroup,
    Input,
    Row
} from "design-react-kit";
import React, { FC, useEffect, useRef, useState } from "react";

interface Message {
    id: number;
    text: string;
    sender: 'user' | 'bot';
}

export const Chat: FC = () => {
    const [messages, setMessages] = useState<Message[]>([]);
    const [inputValue, setInputValue] = useState<string>('');
    const [socket, setSocket] = useState<WebSocket | null>(null);
    const socketRef = useRef<WebSocket | null>(null);

    const [isTyping, setIsTyping] = useState<Boolean>(false);
  
    useEffect(() => {
      // Create WebSocket connection
      const ws = new WebSocket('ws://localhost:8000/ws');
      
      ws.onopen = () => {
        console.log('Connected to WebSocket');
        socketRef.current = ws;
        setSocket(ws);
      };
  
      ws.onmessage = (event: MessageEvent) => {
        const data = JSON.parse(event.data);
        setMessages((prev: Message[]) => [...prev, {
          id: prev.length,
          text: data.message.llm_response.info,
          sender: 'bot'
        }]);
        setIsTyping(false);
      };
  
      ws.onerror = (error: Event) => {
        console.error('WebSocket error:', error);
      };
  
      ws.onclose = () => {
        console.log('Disconnected from WebSocket');
      };
  
      // Cleanup on component unmount
      return () => {
        if (socketRef.current) {
          socketRef.current.close();
        }
      };
    }, []);
  
    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
      e.preventDefault();
      if (!inputValue.trim() || !socketRef.current) return;
  
      // Add user message to chat
      const userMessage: Message = {
        id: messages.length,
        text: inputValue,
        sender: 'user'
      };
      setMessages((prev: Message[]) => [...prev, userMessage]);
  
      // Send message to WebSocket server
      socketRef.current.send(inputValue);
      setInputValue('');
      setIsTyping(true);
    };

  return (
    <Card 
      className="shadow-lg card-bg card-big"
    //   style={{ 
    //     width: '380px',  // Fixed width
    //     margin: '0 auto' 
    //   }}
    >
      <CardBody className="d-flex flex-column">        
        {/* Chat Messages Area */}
        <div 
          className="chat-messages flex-grow-1 overflow-auto mb-3" 
          style={{ 
            border: '1px solid #e0e0e0', 
            borderRadius: '4px',
            padding: '10px'
          }}
        >
          {messages.map((message: Message) => (
            <div 
              key={message.id} 
              className={`message mb-2 ${message.sender === 'user' ? 'text-end' : 'text-start'}`}
            >
              <span 
                className={`
                  p-2 
                  rounded 
                  ${message.sender === 'user' 
                    ? 'bg-primary text-white' 
                    : 'bg-light text-dark'}
                `}
                style={{ 
                  display: 'inline-block',
                  maxWidth: '80%'
                }}
              >
                {message.text}
              </span>
            </div>
          ))}
          
          {isTyping && (
            <div className="text-start">
              <span className="p-2 rounded bg-light text-dark">
                Sto scrivendo...
              </span>
            </div>
          )}
          {/* <div ref={messagesEndRef} /> */}
        </div>

        {/* Message Input */}
        <Form 
          onSubmit={(e) => {
            e.preventDefault();
            handleSubmit(e);
          }}
          className="mt-auto"
        >
          <Row>
            <Col md={9}>
              <FormGroup>
                <Input
                  id="chat-input"
                  type="text"
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  placeholder="Scrivi un messaggio..."
                />
              </FormGroup>
            </Col>
            <Col md={3}>
              <Button 
                color="primary" 
                type="submit" 
                disabled={inputValue.trim() === ""}
                block
              >
                Invia
              </Button>
            </Col>
          </Row>
        </Form>
      </CardBody>
    </Card>
  );
};