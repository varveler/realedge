import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchGroupedTradesDetails, submitComment, changeComment, fetchOrders, cleanGroupedTradesDetailsFetchStatus, cleanFetchOrdersStatus } from './tradesSlicer';
import Grid from '@material-ui/core/Grid';
import { makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import { useRouter } from 'next/router'
import TradeChartWrapper from '../charts/TradeChartWrapper';
import { timeParse } from "d3-time-format";
import { navbarSelected, selectActiveTab } from '../navbar/navBarSlicer'
import { selectUserIsLogedIn} from '../access/accessSlicer'
import TextField from '@material-ui/core/TextField';
import Button from  '@material-ui/core/Button';
import { fetchBarsTrade, setFetchChartStatus, setFromTo, cleanFromTo } from '../charts/chartsSlicer';
import TradesDetailsTables from './TradesDetailsTables'
import {fetchGapper} from '../gappers/gappersSlicer';
import TopTableGapperDetail from '../gappers/TopTableGapperDetail';
import NewsTable from '../news/NewsTable'
import {fromGpedSlugToStartEndDates} from '../../components/helpers'
import CommentsForm from '../logs/CommentsForm'
import TagsForm from '../logs/TagsForm'


const useStyles = makeStyles((theme) => ({
  containerDetail:{
    marginTop: '20px'
  },
  profit:{
    fontSize: '2.5rem',
    color: 'green'
},
  loss: {
    fontSize: '2.5rem',
    color: 'red'
},
  ticker: {
    fontSize: '2.5rem'
  },
  infoTitle:{
    color: 'gray',
    fontSize: '1rem'
  },
  infoTitleTable:{
    color: 'gray',
    fontSize: '1rem',
    textAlign: 'center'
  },

  percentage: {
    fontSize: '1.5rem',
    color: 'green',
    marginTop: '10px'
  },
  cell: {
    textAlign: 'center'
  },
  cellTicker: {
    textAlign: 'center',
    cursor: 'pointer'
  },
  cellheaderTitle: {
    textAlign: 'center',
    whiteSpace: 'nowrap'
  },
  tableContainer: {
    marginTop: '35px'
  },
  tradeComents: {
    marginTop: '25px'
  }
}))

export default function TradeDetail(){
  const router = useRouter();
  const classes = useStyles();
  const dispatch = useDispatch();
  const {slug}  = router.query;
  const parseDate = timeParse("%H:%M:%S %Y/%m/%d");
  const tabSelected = useSelector(selectActiveTab);
  const userIsLogedIn = useSelector(selectUserIsLogedIn);
  //const chartData = useSelector(state => state.charts.data)
  //const fetchChartStatus = useSelector(state => state.charts.status)
  const gapper = useSelector(state => state.gappers.selected)
  const {fetchGroupedTradesDetailsStatus,
        fetchOrdersStatus,
        orders,
        detailGroupedTrades,
        groupedDetails} = useSelector(state => state.trades)



  useEffect(() => {
    if(tabSelected != 1 && userIsLogedIn == true)
      dispatch(navbarSelected(1))
    return function cleanup() {
      //dispatch(setFetchChartStatus('idle'))
      dispatch(cleanGroupedTradesDetailsFetchStatus('idle'))
      dispatch(cleanFetchOrdersStatus('idle'))
      dispatch(cleanFromTo())
    };

  },[])
  useEffect(() => {
    if(slug != undefined) {
      dispatch(fetchGroupedTradesDetails(slug))
      var {from, to} = fromGpedSlugToStartEndDates(slug)
      dispatch(setFromTo({from: from, to: to}))
    }
  },[slug])

  useEffect(() => {
    if(fetchGroupedTradesDetailsStatus === 'succeeded' && fetchOrdersStatus === 'idle'){
      const uuids = [];
      detailGroupedTrades.forEach((trade, i) => {
        uuids.push(trade.uuid)
      });
      dispatch(fetchOrders(uuids))
      dispatch(fetchGapper(`${groupedDetails[0].ticker}-${groupedDetails[0].date.replace('-', '').replace('-', '')}`))
    }
    // if(detailGroupedTrades && detailGroupedTrades.length >= 1 && fetchChartStatus == 'idle' ){
    //   dispatch(fetchBarsTrade(uuids))
    // }
  },[detailGroupedTrades])


  // const filledOrders = orders.length >= 1 ? orders.filter(
  //   order => order.status === "FI").map(
  //     order => {
  //               let parsedDate = parseDate(order.last_time)
  //               const norder = {...order, date: parsedDate, price: parseFloat(order.price)}
  //               return norder
  //     }
  //   )
  // : []

  const renderGroupedTradeDetails = (groupedDetails, detailGroupedTrades) => {
  const uuids = [];
  if(detailGroupedTrades.length >= 1){
    detailGroupedTrades.forEach((trade, i) => {
      uuids.push(trade.uuid)
    });
  }
  return(
    <div className={classes.containerDetail}>
      <Grid container spacing={1}>
        <Grid item xs={2}>
        </Grid>
        <Grid item xs={8}>
            <Grid container spacing={1}>
              <Grid item xs={3}>
                {groupedDetails.pnl > 0 ?
                  <Typography className={classes.profit} component='h1'>{groupedDetails.pnl}<span className={classes.infoTitle}>{' '}profit</span></Typography>
                : <Typography className={classes.loss} component='h1'>{groupedDetails.pnl}<span className={classes.infoTitle}>{' '}loss</span></Typography>
                }
                <Typography className={classes.info} component='p'><span className={classes.infoTitle}>on{' '}</span>{groupedDetails.ticker} <span className={classes.infoTitle}>{' '}{groupedDetails.natural_time}</span></Typography>
                <Typography className={classes.info} component='p'><span className={classes.infoTitle}>with{' '}</span>{groupedDetails.trades_count} <span className={classes.infoTitle}>{groupedDetails.trades_count == 1 ? 'trade' : 'trades'}</span></Typography>
              </Grid>
              <Grid item xs={9}>
                {gapper ? <TopTableGapperDetail gapper={gapper}/> : null }
              </Grid>
            </Grid>
      </Grid>
      <Grid item xs={2}>
      </Grid>
    </Grid>
      <Grid container spacing={1}>
        <Grid item xs={1}>
        </Grid>
        <Grid item xs={10}>
          {/* uuids.length >= 1 ? <TradeChartWrapper uuids={uuids} timeFrame={'1Min'}/> : null }
          {uuids.length >= 1 ? <TradeChartWrapper uuids={uuids} timeFrame={'1Day'}/> : null */}
          <TradesDetailsTables groupedTradesDetails={groupedDetails} trades={groupedDetails.trades} orders={orders} />
          <TagsForm ticker={groupedDetails.ticker} date={groupedDetails.date}/>
          <CommentsForm ticker={groupedDetails.ticker} date={groupedDetails.date} />
          {/* <NewsTable ticker={slug.split('-')[0]} />
            {/*<TextField
            className={classes.tradeComents}
            id="outlined-multiline-static"
            label="Trade Comments"
            fullWidth
            multiline
            rows={4}
            variant="outlined"
            value={groupedDetails.comments}
            onChange={event => dispatch(changeComment(event.target.value))}
          />
          <Button onClick={(event) => {event.preventDefault; dispatch(submitComment({uuid:groupedDetails.uuid, comment:tradeSelected.comments}))}} variant="contained" color="primary">
            Save
          </Button> /*/}
        </Grid>
        <Grid item xs={1}>
        </Grid>
      </Grid>
    </div>
  )}
  const renderNoTradeSelected = () => <p> Loading Data.... </p>

  return(
    <div>
      {detailGroupedTrades && detailGroupedTrades.length >= 1 ? renderGroupedTradeDetails(groupedDetails[0], detailGroupedTrades) : renderNoTradeSelected}
    </div>
  )
}
