import React from "react";
import PropTypes from "prop-types";

class DataWrapper extends React.Component {
	render() {
		return(
			this.props.children
		);
	}
	getChildContext() {
		const { childData } = this.props;
		return {
			plotData: childData
		};
	}
}
DataWrapper.childContextTypes= {
    plotData: PropTypes.array,
}

export {DataWrapper};
