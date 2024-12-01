import "bootstrap-italia/dist/css/bootstrap-italia.min.css";
import { FC } from "react";
import "./App.css";
import { Chat } from "./Chat";
import { CompleteHeader } from "./components";

export const App: FC = () => {

	return (
		<div>
			<CompleteHeader />
			<div className="container">
                <div className="row justify-content-center">
                    <div className="col-lg-12 col-md-10 col-sm-12">
                        <Chat />
                    </div>
                </div>
            </div>
		</div>
	);
};

export default App;
