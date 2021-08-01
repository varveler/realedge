import React from 'react';
import Chart2 from './Chart2';
import { TypeChooser } from "react-stockcharts/lib/helper";
import { connect } from 'react-redux';
import { fetchBarsGapper } from './chartsSlicer';
import { timeParse } from "d3-time-format";

//https://data.alpaca.markets//v2/stocks/AAPL/bars?start=2021-04-06T09:01:00Z&end=2021-04-10T22:01:00Z&timeframe=1Min
//timeframe, ticker, start_time, end_time
class GapperChartWrapper extends React.Component {
  constructor(props){
    super(props);
  }

	componentDidMount() {
		this.props.dispatch(fetchBarsGapper({slug: this.props.slug }))
	}
	render() {
		if ( this.props.data.length == 0) {
			return <div>Loading...</div>
		}
    var maxHigh = Math.max.apply(Math, this.props.data.map(function(x) { return x.high; })) * 1.5
    const bars = this.props.data.map(
      function(el){
        const parsed = new Date(el.date)
        var minute = parsed.getHours() * 60 + parsed.getMinutes()
        var marketOpenMinute = 510 // (9*60) + 30
        var marketCloseMinute = 899 // (15*60) -1
        if (minute >= marketOpenMinute &&
            minute <= marketCloseMinute) {
            return {...el, date: parsed, shadowPremarket:null}
        }else{
          return {...el, date: parsed, shadowPremarket:maxHigh}
        }
      }
    )
		return (
        <Chart2 type={'svg'} data={bars} />
		)
	}
}


const mapStateToProps = (state) => ({
  data: state.charts.data
});



export default connect(mapStateToProps)(GapperChartWrapper);
