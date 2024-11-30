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
  data_ora?: { [key: string]: string[] }; // Aggiunto per gestire date e orari
}

export const Chat: FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState<string>('');
  const socketRef = useRef<WebSocket | null>(null);
  const [isTyping, setIsTyping] = useState<boolean>(false);

  useEffect(() => {
    // Creazione della connessione WebSocket
    const ws = new WebSocket('ws://localhost:8000/ws');

    ws.onopen = () => {
      console.log('Connected to WebSocket');
      socketRef.current = ws;
    };

    ws.onmessage = (event: MessageEvent) => {
      const data = JSON.parse(event.data);

      setMessages((prev: Message[]) => [
        ...prev,
        {
          id: prev.length,
          text: data.message.llm_response.info,
          sender: 'bot',
          data_ora: data.message.response // Gestione delle date e orari
        }
      ]);

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
        socketRef.current = null;
      }
    };
  }, []);

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!inputValue.trim() || !socketRef.current) return;

    const userMessage: Message = {
      id: messages.length,
      text: inputValue,
      sender: 'user'
    };

    setMessages((prev: Message[]) => [...prev, userMessage]);
    socketRef.current?.send(inputValue);
    setInputValue('');
    setIsTyping(true);
  };

  return (
    <Card className="shadow-lg card-bg card-big">
      <CardBody className="d-flex flex-column">
        {/* Area dei messaggi */}
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

                {/* Rendering dei bottoni per date e orari */}
                {message.sender === 'bot' &&
                  message.data_ora &&
                  Object.keys(message.data_ora).length > 0 && (
                    <div className="mt-2 d-flex flex-wrap justify-content-start gap-2">
                      {Object.entries(message.data_ora).map(([date, times]) =>
                        times.map((time, index) => (
                          <Button
                            key={`${date}-${index}`}
                            color="secondary"
                            outline
                            size="sm"
                            onClick={() => console.log(`Selezionato: ${date} ${time}`)}
                          >
                            {`${date} ${time}`}
                          </Button>
                        ))
                      )}
                    </div>
                  )}
              </span>
            </div>
          ))}

          {isTyping && (
            <div className="text-start">
              <span className="p-2 rounded bg-light text-dark">Sto scrivendo...</span>
            </div>
          )}
        </div>

        {/* Input del messaggio */}
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
