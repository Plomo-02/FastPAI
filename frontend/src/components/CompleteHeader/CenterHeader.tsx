import { Header, HeaderBrand, HeaderContent, HeaderRightZone, HeaderSocialsZone, Icon } from "design-react-kit";
import { FC } from "react";

type Props = any;

export const CenterHeader: FC<Props> = ({ props }) => {
	return (
		<Header type="center" theme={props?.theme}>
			<HeaderContent>
				<HeaderBrand iconName={props?.iconName} iconAlt={props?.iconAlt || ""}>
					<h2>FastPAI</h2>
					<h3>F4 PAsiti</h3>
				</HeaderBrand>
				<HeaderRightZone>
					<HeaderSocialsZone label="Source code on">
						<ul>
							<li>
								<a href="#" aria-label="Github" target="https://github.com/Plomo-02/FastPAI">
									<Icon icon="it-github" />
								</a>
							</li>
						</ul>
					</HeaderSocialsZone>
				</HeaderRightZone>
			</HeaderContent>
		</Header>
	);
};
