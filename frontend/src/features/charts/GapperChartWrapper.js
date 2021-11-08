import React, { useEffect } from 'react';
import Chart from './Chart';
import { useSelector, useDispatch } from 'react-redux';
import { connect } from 'react-redux';
import { fetchBarsGapper, setFetchChartStatus } from './chartsSlicer';
import { timeParse } from "d3-time-format";
import CircularProgress from '@material-ui/core/CircularProgress';
import Grid from '@material-ui/core/Grid';


export default function GapperChartWrapper ({slug, timeFrame, ticker}){
  const dispatch = useDispatch()
  const data = useSelector(state => state.charts.data[timeFrame])
  const {status} = useSelector(state => state.charts)

  useEffect(() => {
    if(status == 'idle'){
      dispatch(fetchBarsGapper({slug: slug, timeFrame: timeFrame}))
    }
    return function cleanup() {
      dispatch(setFetchChartStatus('idle'))
    };
  },[])

  // useEffect(() => {
  //   if(id != undefined) {
  //
  //   }
  // },[id])
  if (data == undefined) return <p>Unable to load {timeFrame} chart.</p>
  if ( data.length == 0 ) {
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
  if(timeFrame == '1Min'){
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
        <Chart type={'svg'} data={bars} timeFrame={timeFrame} intraday ticker={ticker} />
    )
  }else{
    const bars = data.map(
      function(el){
        const parsed = new Date(el.date)
        return {...el, date: parsed}
      }
    )
    return (
        <Chart type={'svg'} timeFrame={'Day'} data={bars} ticker={ticker} />
    )
  }

}
