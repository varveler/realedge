import React from "react";
import PropTypes from "prop-types";
import withStyles from "@material-ui/core/styles/withStyles";
import { format } from "d3-format";
import { curveMonotoneX } from "d3-shape";
import { timeFormat } from "d3-time-format";

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

import { discontinuousTimeScaleProvider } from "react-stockcharts/lib/scale";
import { fitWidth } from "react-stockcharts/lib/helper";
import { last } from "react-stockcharts/lib/utils";
import { createVerticalLinearGradient, hexToRGBA } from "react-stockcharts/lib/utils";

import {DataWrapper} from "./DataWrapper";

import { OHLCTooltip } from "react-stockcharts/lib/tooltip";

const style = {
  triangleMarker:{
		color: 'pink'
  }
}



class CandleStickStockScaleChartWithVolumeBarV3 extends React.Component {
	render() {
		const { type, data: initialData, width, ratio, classes, filledOrders } = this.props;
		const xScaleProvider = discontinuousTimeScaleProvider
			.inputDateAccessor(d => d.date);
		const {
			data,
			xScale,
			xAccessor,
			displayXAccessor,
		} = xScaleProvider(initialData);


		const start = xAccessor(last(data));
		const end = xAccessor(data[Math.max(0, data.length - 700)]);
		//const end = xAccessor(data.filter(el => el.entryShort != null || el.entryLong != null)[0])
		const xExtents = [start, end];



		return (
			<ChartCanvas height={600}
				ratio={ratio}
				width={width}
				margin={{ left: 50, right: 50, top: 10, bottom: 30 }}
				type={type}
				seriesName="MSFT"
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
					<YAxis axisAt="right" orient="right" ticks={5} />
					<XAxis axisAt="bottom" orient="bottom" showTicks={false}/>
					<MouseCoordinateX
						rectWidth={60}
						at="bottom"
						orient="bottom"
						displayFormat={timeFormat("%H:%M:%S")} />
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
				</Chart>
				<CrossHairCursor />
				<Chart id={2} origin={(w, h) => [0, h - 150]} height={150} yExtents={d => d.volume}>
					<XAxis axisAt="bottom" orient="bottom"/>
					<YAxis axisAt="left" orient="left" ticks={5} tickFormat={format(".2s")}/>
					<BarSeries yAccessor={d => d.volume} fill={(d) => d.close > d.open ? "#6BA583" : "red"} />
				</Chart>
			</ChartCanvas>
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
