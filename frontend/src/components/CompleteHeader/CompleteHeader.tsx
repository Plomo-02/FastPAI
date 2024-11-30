import { Headers } from "design-react-kit";
import { FC } from "react";
import { CenterHeader } from "./CenterHeader";
import { SlimHeader } from "./SlimHeader";

export const CompleteHeader: FC = () => {
	return (
		<Headers sticky={true}>
			<div className="it-nav-wrapper">
				<CenterHeader />
				{/* <NavHeader /> */}
			</div>
		</Headers>
	);
};
