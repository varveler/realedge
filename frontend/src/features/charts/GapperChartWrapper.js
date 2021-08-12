import React from 'react';
import Chart2 from './Chart2';
import { TypeChooser } from "react-stockcharts/lib/helper";
import { connect } from 'react-redux';
import { fetchBarsGapper } from './chartsSlicer';
import { timeParse } from "d3-time-format";
import CircularProgress from '@material-ui/core/CircularProgress';
import Grid from '@material-ui/core/Grid';

//https://data.alpaca.markets//v2/stocks/AAPL/bars?start=2021-04-06T09:01:00Z&end=2021-04-10T22:01:00Z&timeframe=1Min
//timeframe, ticker, start_time, end_time
class GapperChartWrapper extends React.Component {
  constructor(props){
    super(props);
  }

	// componentDidMount() {
	// 	this.props.dispatch(fetchBarsGapper({slug: this.props.slug }))
	// }
	render() {
    const { data } = this.props;
		if ( data.length == 0) {
			return (
        <div style={{height: '200px', marginTop:'150px'}}>
          <Grid  container
            direction="row"
            justifyContent="space-between"
            alignItems="stretch">
            <Grid item xs={6}>
            </Grid>
            <Grid item xs={3} >
              <CircularProgress/>
            </Grid>
            <Grid item xs={3}>
            </Grid>
          </Grid>
        </div>
      )
		}
    var maxHigh = Math.max.apply(Math, data.map(function(x) { return x.high; })) * 1.5
    const bars = data.map(
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
