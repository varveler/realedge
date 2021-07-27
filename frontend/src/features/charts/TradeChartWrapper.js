import React from 'react';
import Chart2 from './Chart2';
import { TypeChooser } from "react-stockcharts/lib/helper";
import { connect } from 'react-redux';
import { fetchBarsTrade } from './chartsSlicer';
import { timeParse } from "d3-time-format";

//https://data.alpaca.markets//v2/stocks/AAPL/bars?start=2021-04-06T09:01:00Z&end=2021-04-10T22:01:00Z&timeframe=1Min
//timeframe, ticker, start_time, end_time
class ChartWrapper extends React.Component {
  constructor(props){
    super(props);
  }

	componentDidMount() {
		this.props.dispatch(fetchBarsTrade({uuid: this.props.uuid }))
	}
	render() {
    const { filledOrders } = this.props;
		if ( this.props.data.length === 0) {
			return <div>Loading...</div>
		}
    const bars = this.props.data.map(
      function(el){
        const parsed = new Date(el.date)
        let newob = {...el, date: parsed};
        return newob
      }
    )
		return (
        <Chart2 type={'svg'} data={bars} filledOrders={filledOrders} />
		)
	}
}


const mapStateToProps = (state) => ({
  data: state.charts.data
});



export default connect(mapStateToProps)(ChartWrapper);
