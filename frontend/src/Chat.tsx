import {
  Button,
  Card,
  CardBody,
  Col,
  Form,
  FormGroup,
  Input,
  Modal,
  ModalBody,
  ModalFooter,
  ModalHeader,
  Row
} from "design-react-kit";
import React, { FC, useEffect, useRef, useState } from "react";

interface Message {
  id: number;
  text: string;
  sender: 'user' | 'bot';
  data_ora?: { [key: string]: string[] };
}

export const Chat: FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState<string>('');
  const socketRef = useRef<WebSocket | null>(null);
  const [isTyping, setIsTyping] = useState<boolean>(false);

  // Stato per la modale
  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
  const [selectedAppointment, setSelectedAppointment] = useState<string | null>(null);

  // Stato per la modale di selezione città
  const [isCityModalOpen, setIsCityModalOpen] = useState<boolean>(true);
  const [selectedCity, setSelectedCity] = useState<string | null>(null);

  // Stato per il banner di conferma
  const [showAlert, setShowAlert] = useState<boolean>(false);

  // Stato per gli appuntamenti confermati
  const [confirmedAppointments, setConfirmedAppointments] = useState<string[]>([]);

  // Stato per l'hover sui bottoni
  const [hoveredButton, setHoveredButton] = useState<string | null>(null);

  useEffect(() => {
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
          data_ora: data.message.response
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
    socketRef.current?.send(JSON.stringify({ message: inputValue, city: selectedCity }));
    setInputValue('');
    setIsTyping(true);
  };

  const toggleModal = () => setIsModalOpen(!isModalOpen);

  const handleAppointmentClick = (appointment: string) => {
    setSelectedAppointment(appointment);
    toggleModal();
  };

  const handleShowAlert = () => {
    setShowAlert(true);
    setTimeout(() => setShowAlert(false), 3000); // Nasconde il banner dopo 3 secondi
  };

  const handleConfirm = () => {
    if (selectedAppointment) {
      setConfirmedAppointments((prev) => [...prev, selectedAppointment]); // Aggiungi l'appuntamento confermato
    }
    toggleModal();
    handleShowAlert();
  };

  const handleCitySelect = (city: string) => {
    setSelectedCity(city);
    setIsCityModalOpen(false); // Chiudi la modale
  };

  const handleMouseEnter = (key: string) => setHoveredButton(key);
  const handleMouseLeave = () => setHoveredButton(null);

  const buttonStyle = (key: string, disabled: boolean) => ({
    transition: 'background-color 0.3s ease, color 0.3s ease',
    backgroundColor: disabled
      ? '#f8f9fa'
      : hoveredButton === key
      ? '#0066CC'
      : '#ffffff',
    color: disabled ? '#6c757d' : hoveredButton === key ? '#ffffff' : '#0066CC',
    borderColor: disabled ? '#ced4da' : hoveredButton === key ? '#004C99' : '#0066CC',
    cursor: disabled ? 'not-allowed' : 'pointer',
    opacity: disabled ? 0.6 : 1
  });

  return (
    <>
      {/* Modale per selezionare una città */}
<Modal isOpen={isCityModalOpen} toggle={() => setIsCityModalOpen(!isCityModalOpen)}>
  <ModalHeader toggle={() => setIsCityModalOpen(!isCityModalOpen)}>
    Seleziona una Città
  </ModalHeader>
  <ModalBody>
    Scegli la tua città per continuare:
    <div className="mt-3 d-flex flex-column gap-2">
      <Button color="primary" onClick={() => handleCitySelect('Bari')}>
        Bari
      </Button>
      <Button color="primary" onClick={() => handleCitySelect('Napoli')}>
        Napoli
      </Button>
      <Button color="primary" onClick={() => handleCitySelect('Roma')}>
        Roma
      </Button>
    </div>
  </ModalBody>
  <ModalFooter>
  </ModalFooter>
</Modal>


      <Card className="shadow-lg card-bg my-4">
        <CardBody className="d-flex flex-column" style={{ height: '70vh' }}>
          {/* Area dei messaggi */}
          <div
            className="chat-messages flex-grow-1 overflow-auto mb-3"
            style={{
              border: '1px solid #e0e0e0',
              borderRadius: '14px',
              padding: '15px',
              backgroundColor: '#f8f9fa'
            }}
          >
            {messages.map((message: Message) => (
              <div
                key={message.id}
                className={`message mb-3 ${message.sender === 'user' ? 'text-end' : 'text-start'}`}
              >
                <span
                  className={`
                    p-3 
                    ${message.sender === 'user'
                      ? 'bg-primary text-white'
                      : 'bg-white text-dark shadow-sm'}
                  `}
                  style={{
                    display: 'inline-block',
                    maxWidth: '70%',
                    wordWrap: 'break-word',
                    borderRadius: '14px'
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
                              color="primary"
                              outline
                              size="sm"
                              onMouseEnter={() => handleMouseEnter(`${date}-${index}`)}
                              onMouseLeave={handleMouseLeave}
                              onClick={() => handleAppointmentClick(`${date} ${time}`)}
                              disabled={confirmedAppointments.includes(`${date} ${time}`)}
                              style={buttonStyle(`${date}-${index}`, confirmedAppointments.includes(`${date} ${time}`))}
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
                <span className="p-2 rounded bg-light text-dark">
                  Sto scrivendo
                  <span className="typing-dots">
                    <span>.</span><span>.</span><span>.</span>
                  </span>
                </span>
              </div>
            )}
          </div>

          {/* Input del messaggio */}
          <Form onSubmit={handleSubmit} className="mt-auto">
            <Row className="g-2">
              <Col>
                <FormGroup className="mb-0">
                  <Input
                    id="chat-input"
                    type="text"
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    placeholder="Scrivi un messaggio..."
                    className="rounded-pill border-2"
                    style={{ padding: '0.75rem 1.5rem' }}
                  />
                </FormGroup>
              </Col>
              <Col xs="auto">
                <Button
                  color="primary"
                  type="submit"
                  disabled={inputValue.trim() === ""}
                  className="rounded-pill px-4"
                >
                  Invia
                </Button>
              </Col>
            </Row>
          </Form>
        </CardBody>

        {/* Modale per confermare l'appuntamento */}
        <Modal isOpen={isModalOpen} toggle={toggleModal}>
          <ModalHeader toggle={toggleModal}>Conferma Appuntamento</ModalHeader>
          <ModalBody>
            Sei sicuro di voler confermare l'appuntamento selezionato: <strong>{selectedAppointment}</strong>?
          </ModalBody>
          <ModalFooter>
            <Button color="primary" onClick={handleConfirm}>
              Conferma
            </Button>
            <Button color="secondary" outline onClick={toggleModal}>
              Annulla
            </Button>
          </ModalFooter>
        </Modal>

        {/* Banner di conferma */}
        {showAlert && (
          <div
            className="position-fixed top-0 start-50 translate-middle-x alert alert-success shadow-lg"
            style={{
              zIndex: 1050,
              maxWidth: '90%',
              animation: 'fade-in-out 3s'
            }}
          >
            Appuntamento confermato con successo!
          </div>
        )}
      </Card>
    </>
  );
};