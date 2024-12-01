import { Header, HeaderBrand, HeaderContent, HeaderRightZone, Icon } from "design-react-kit";
import { FC } from "react";

type Props = any;

export const CenterHeader: FC<Props> = ({ props }) => {
	return (
		<Header type="center" theme={props?.theme}>
			<HeaderContent>
        <HeaderBrand iconName="./logo.svg" iconAlt="FastPAI">
          <h2>FastPAI</h2>
          <span>F4 Basiti</span>
        </HeaderBrand>
				<HeaderRightZone>
          <a
              href="https://github.com/Plomo-02/FastPAI"
              aria-label="Github"
              target="_blank"
              rel="noopener noreferrer"
              style={{
                textDecoration: "none",
                color: "#ffffff", // Testo bianco
                fontWeight: "bold",
              }}
            >
            <span style={{ marginRight: "8px" }}>Source code on</span>
            <Icon icon="it-github" color="white" />
          </a>
        </HeaderRightZone>
			</HeaderContent>
		</Header>
	);
};