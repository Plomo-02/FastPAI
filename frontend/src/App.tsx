import "bootstrap-italia/dist/css/bootstrap-italia.min.css";
import { FC } from "react";
import "./App.css";
import { Chat } from "./Chat";
import { CompleteHeader } from "./components";

export const App: FC = () => {

	return (
		<div>
			<CompleteHeader />
			<div className="container my-4">
				<div className="my-4">
				</div>
			</div>
			<Chat />
		</div>
	);
};

export default App;
