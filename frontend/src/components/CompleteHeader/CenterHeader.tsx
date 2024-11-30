import { Header, Icon } from "design-react-kit";
import { FC } from "react";

type Props = any;

export const CenterHeader: FC<Props> = ({ props }) => {
  return (
    <header
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "0 20px",
        height: "100px", // Altezza fissa del header
        backgroundColor: "#0066CC", // Colore dello sfondo
        color: "#ffffff", // Testo in bianco
        boxShadow: "0px 2px 4px rgba(0, 0, 0, 0.1)"
      }}
    >
      {/* Sottotitolo F4 Basiti a sinistra */}
      <div style={{ flex: 1, textAlign: "left" }}>
        <h3
          style={{
            fontSize: "1.2rem",
            margin: "0",
            fontWeight: "normal",
            textAlign: "left",
            color: "#ffffff" // Testo bianco
          }}
        >
          F4 Basiti
        </h3>
      </div>

      {/* Titolo FastPAI centrato */}
      <div style={{ flex: 2, textAlign: "center" }}>
        <h1
          style={{
            fontSize: "2.5rem",
            margin: "0",
            fontWeight: "bold",
            textAlign: "center",
            color: "#ffffff" // Testo bianco
          }}
        >
          FastPAI
        </h1>
      </div>

      {/* Etichetta "Source code on" con icona GitHub a destra */}
      <div style={{ flex: 1, textAlign: "right" }}>
        <a
          href="https://github.com/Plomo-02/FastPAI"
          aria-label="Github"
          target="_blank"
          rel="noopener noreferrer"
          style={{
            textDecoration: "none",
            color: "#ffffff", // Testo bianco
            fontWeight: "bold",
            display: "flex",
            alignItems: "center",
            justifyContent: "flex-end" // Allinea tutto a destra
          }}
        >
          <span style={{ marginRight: "8px" }}>Source code on</span>
          <Icon icon="it-github" style={{ fontSize: "1.5rem", color: "#ffffff" }} />
        </a>
      </div>
    </header>
  );
};
