import React, { Fragment, useEffect, useState } from 'react';
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
    color: '#00af83',
    marginRight: '5px'
},
  loss: {
    fontSize: '2.5rem',
    color: '#fc5a6d',
    marginRight: '5px'
},
  ticker: {
    fontSize: '2.5rem'
  },
  infoTitle:{
    color: 'gray',
    fontSize: '1rem',
    marginRight: '5px'
  },
  infoTitleTable:{
    color: 'gray',
    fontSize: '1rem',
    textAlign: 'center'
  },
  info:{
    marginRight: '5px'
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
  const {from, to} = useSelector(state => state.charts)
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
              <Grid
                xs={3}
                item
                container
                direction="row"
                justifyContent="space-between"
                alignItems="baseline"
              >
                {groupedDetails.pnl > 0 ?
                  <Fragment>
                    <Typography className={classes.profit} component='h1'>
                      {groupedDetails.pnl}
                    </Typography>
                    <Typography className={classes.infoTitle}>
                      profit on
                    </Typography>
                  </Fragment>
                : <Fragment>
                    <Typography className={classes.loss} component='h1'>
                      {groupedDetails.pnl}
                    </Typography>
                    <Typography className={classes.infoTitle}>
                      loss on
                    </Typography>
                  </Fragment>
                }
                <Typography className={classes.info} component='p'>
                  {groupedDetails.ticker}
                </Typography>
                <span className={classes.infoTitle}>
                  with{' '}
                  {groupedDetails.trades_count}
                  {groupedDetails.trades_count == 1 ? ' trade' : ' trades'}
                </span>
                <Grid item xs={9}>
                  {gapper ? <TopTableGapperDetail gapper={gapper}/> : null }
                </Grid>
              </Grid>
            </Grid>
      </Grid>
      <Grid item xs={2}>
      </Grid>
    </Grid>
      <Grid container spacing={1}>
        <Grid item xs={2}>
        </Grid>
        <Grid item xs={8}>
          <TagsForm ticker={groupedDetails.ticker} date={groupedDetails.date}/>
          <CommentsForm ticker={groupedDetails.ticker} date={groupedDetails.date} />
          <TradesDetailsTables groupedTradesDetails={groupedDetails} trades={groupedDetails.trades} orders={orders} />
          { uuids.length >= 1 ? <TradeChartWrapper uuids={uuids} ticker={groupedDetails.ticker} timeFrame={'1Min'}/> : null }
          {uuids.length >= 1 ? <TradeChartWrapper uuids={uuids} ticker={groupedDetails.ticker} timeFrame={'1Day'}/> : null }
          <NewsTable _from={from} to={to} ticker={slug.split('-')[0]} />
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
        <Grid item xs={2}>
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
