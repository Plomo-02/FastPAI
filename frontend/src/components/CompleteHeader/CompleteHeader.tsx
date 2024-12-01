import { Headers } from "design-react-kit";
import { FC } from "react";
import { CenterHeader } from "./CenterHeader";

export const CompleteHeader: FC = () => {
	return (
		<Headers sticky={true}>
			<div className="it-nav-wrapper">
				<CenterHeader small={true}/>
				{/* <NavHeader /> */}
			</div>
		</Headers>
	);
};
