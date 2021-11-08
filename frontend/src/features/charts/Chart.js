import React, {Fragment} from "react";
import PropTypes from "prop-types";
import withStyles from "@material-ui/core/styles/withStyles";
import { format } from "d3-format";
import { curveMonotoneX } from "d3-shape";
import { timeFormat } from "d3-time-format";
import Paper from '@material-ui/core/Paper';
import Box from '@material-ui/core/Box';
import Typography from '@material-ui/core/Typography';

import { ChartCanvas, Chart } from "react-stockcharts";
import {
	BarSeries,
	CandlestickSeries,
  ScatterSeries,
	TriangleMarker,
	LineSeries,
	CircleMarker,
	AreaSeries
} from "react-stockcharts/lib/series";

import {
	CrossHairCursor,
	EdgeIndicator,
	CurrentCoordinate,
	MouseCoordinateX,
	MouseCoordinateY
} from "react-stockcharts/lib/coordinates";

import { XAxis, YAxis } from "react-stockcharts/lib/axes";
import { LabelAnnotation, Label, Annotate } from "react-stockcharts/lib/annotation";
import { discontinuousTimeScaleProvider } from "react-stockcharts/lib/scale";
import { fitWidth } from "react-stockcharts/lib/helper";
import { last } from "react-stockcharts/lib/utils";
import { createVerticalLinearGradient, hexToRGBA } from "react-stockcharts/lib/utils";

import {DataWrapper} from "./DataWrapper";

import { OHLCTooltip } from "react-stockcharts/lib/tooltip";

const style = {
  triangleMarker:{
		color: 'pink'
  },
	wrapper:{
		marginTop:'10px'
	},
	infoTitle:{
		color: 'gray',
		fontSize: '1rem'
	},
}


class CandleStickStockScaleChartWithVolumeBarV3 extends React.Component {
	render() {
		const { type, data: initialData, width, ratio, classes, intraday, timeFrame, ticker } = this.props;
		const xScaleProvider = discontinuousTimeScaleProvider
			.inputDateAccessor(d => d.date);
		const {
			data,
			xScale,
			xAccessor,
			displayXAccessor,
		} = xScaleProvider(initialData);

		let tf;
		if(intraday){
			tf = timeFormat("%H:%M:%S")
		}else{
			tf = timeFormat("%Y-%m-%d")
		}

		const start = xAccessor(last(data));
		const end = xAccessor(data[Math.max(0, data.length - 700)]);
		//const end = xAccessor(data.filter(el => el.entryShort != null || el.entryLong != null)[0])
		const xExtents = [start, end];
		const annotationProps = {
			fontFamily: "Roboto",
			fontSize: 15,
			fontWeight: 600,
			fill: "#060F8F",
			opacity: 0.8,
			text: "N",
			y: ({ yScale }) => yScale.range()[0],
			onClick: console.log.bind(console),
			tooltip: d => d.news,
			onMouseOver: console.log.bind(console)
		};

		return (
			<Fragment>
				<Box pt={4}>
					{intraday ?
						<Typography className={classes.infoTitle} align='center' component='p'>
							{ticker}{' '}one minute chart
						</Typography>
						:
						<Typography className={classes.infoTitle} align='center' component='p'>
							{ticker}{' '}daily chart
						</Typography>
					}
				</Box>
				<Paper  className={classes.wrapper} elevation={2} >
					<ChartCanvas height={600}
						ratio={ratio}
						width={width}
						margin={{ left: 50, right: 50, top: 10, bottom: 30 }}
						type={type}
						data={data}
						xScale={xScale}
						xAccessor={xAccessor}
						displayXAccessor={displayXAccessor}
						xExtents={xExtents}
					>
						<Chart id={1} height={400} yExtents={d => [d.high, d.low]} >
							<defs>
								<linearGradient id="MyGradient" x1="0" y1="100%" x2="0" y2="0%">
									<stop offset="100%" stopColor="#b5d0ff" stopOpacity={0.8} />
									<stop offset="70%" stopColor="#6fa4fc" stopOpacity={0.4} />
									<stop offset="0%"  stopColor="#4286f4" stopOpacity={0.2} />
								</linearGradient>
							</defs>
							<Label x={(width) / 2} y={50}
								fontSize="30" opacity={.20} text={timeFrame} />
							<YAxis axisAt="right" orient="right" ticks={5} />
							<XAxis axisAt="bottom" orient="bottom" showTicks={false}/>
							<MouseCoordinateX
								rectWidth={70}
								at="bottom"
								orient="bottom"
								displayFormat={tf} />
							<MouseCoordinateY
								at="right"
								orient="right"
								displayFormat={format(".2f")} />
							<CandlestickSeries />
		          <DataWrapper childData={data}>
								<ScatterSeries
										yAccessor={d => d.entryShort}
										marker={TriangleMarker}
										markerProps={{
											width:  20,
		                	direction: "bottom",
											stroke: "#ff2626",
											fill: "#ff2626"
										}}
								/>
								<ScatterSeries
										yAccessor={d => d.exitShort}
										marker={TriangleMarker}
										markerProps={{
											width:  20,
											stroke: "#269619",
											fill: "#269619"
										}}
								/>
								<ScatterSeries
								yAccessor={d => d.executionPrice}
								marker={CircleMarker}
								markerProps={{ r: 3 }} />
								<LineSeries
									yAccessor={d => d.vwap_pandas}
									stroke="#FF9535" />
								<LineSeries
									yAccessor={d => d.intradayVwap}
									stroke="#bababa" />
								<AreaSeries
									yAccessor={d => d.shadowPremarket}
									fill="rgba(0, 0, 0, 0.03)"
									strokeWidth={0.01}

								/>
							</DataWrapper>
							<OHLCTooltip origin={[-40, 0]} xDisplayFormat={timeFormat("%Y-%m-%d %H:%M:%S")}/>
							<CurrentCoordinate yAccessor={d => d.volume} fill="#9B0A47" />
							<EdgeIndicator itemType="last" orient="right" edgeAt="right"
								yAccessor={d => d.volume} displayFormat={format(".4s")} fill="#0F0F0F"/>
							<Annotate with={LabelAnnotation}
								when={d => d.news != 0 /* some condition */}
								usingProps={annotationProps} />
						</Chart>
						<CrossHairCursor />
						<Chart id={2} origin={(w, h) => [0, h - 150]} height={150} yExtents={d => d.volume}>
							<XAxis axisAt="bottom" orient="bottom"/>
							<YAxis axisAt="left" orient="left" ticks={5} tickFormat={format(".2s")}/>
							<BarSeries yAccessor={d => d.volume} fill={(d) => d.close > d.open ? "#6BA583" : "red"} />
						</Chart>
					</ChartCanvas>
				</Paper>
			</Fragment>
		);
	}
}
CandleStickStockScaleChartWithVolumeBarV3.propTypes = {
	data: PropTypes.array.isRequired,
	width: PropTypes.number.isRequired,
	ratio: PropTypes.number.isRequired,
	type: PropTypes.oneOf(["svg", "hybrid"]).isRequired,
};

CandleStickStockScaleChartWithVolumeBarV3.defaultProps = {
	type: "svg",
};
CandleStickStockScaleChartWithVolumeBarV3 = fitWidth(CandleStickStockScaleChartWithVolumeBarV3);

export default withStyles(style)(CandleStickStockScaleChartWithVolumeBarV3);
