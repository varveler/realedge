import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { selectTrade, fetchTradesGroupedByTicker, selectAllTrades } from './tradesSlicer';
import { navbarSelected, selectActiveTab } from '../navbar/navBarSlicer'
import { selectUserIsLogedIn} from '../access/accessSlicer'
import { useRouter } from 'next/router'
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
import Link from 'next/link'


const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  paper: {
    padding: theme.spacing(1),
    textAlign: 'center',
    color: theme.palette.text.secondary,
  },
  tableContainer: {
    marginTop: '40px'
  },
  cell: {
    textAlign: 'center'
  },
  cellLink: {
    textAlign: 'center',
    cursor: 'pointer',
    color: 'blue'
  },
  cellheaderTitle: {
    textAlign: 'center',
    whiteSpace: 'nowrap'
  }
}));


export default function ByDayByTrade () {
  const userIsLogedIn = useSelector(selectUserIsLogedIn)
  const dispatch = useDispatch();
  const classes = useStyles();
  const router = useRouter()
  const {groupedFetchStatus, tradesGroupedByTicker} = useSelector(state => state.trades);
  const {groupByTicker} = useSelector(state => state.access);

  let content
  useEffect(() => {
    if (!userIsLogedIn) {
        router.push('/signin')
      } else {
        dispatch(navbarSelected(1))
        if (groupedFetchStatus === 'idle') {
          console.log('groupByTicker', groupByTicker)
          dispatch(fetchTradesGroupedByTicker())
        }
}
  }, [groupedFetchStatus, dispatch]);

  const handleRoute = (e, path) => {
    e.preventDefault()
    router.push(path)

  };


  if (groupedFetchStatus === 'loading') {
    content = <div className="loader">Loading Trades...</div>
  } else if (groupedFetchStatus === 'succeeded' && tradesGroupedByTicker.length >= 1) {
    var dates = [];

    tradesGroupedByTicker.map(trade => {
      let trimedDate = trade.start_time.split('T')[0]
      if(!dates.includes(trimedDate)){dates.push(trimedDate)}})
      var ordererByDayTrades = {}
      dates.forEach((date, i) => {
        var gs = tradesGroupedByTicker.filter(trade => trade.start_time.split('T')[0] === date)
        ordererByDayTrades[date] = gs
    });
    content = dates.map((date, i) => {
      var slDate = date.replace(/-/g, '');
      var renderedTrades = ordererByDayTrades[date].map(trade => {
        var path = `/${trade.slug}`
        return(
        <TableRow key={trade.uuid}>
          <TableCell onClick={ (e) => handleRoute(e, path)} className={classes.cellLink}>
            <a>{trade.ticker}</a>
          </TableCell>
          <TableCell className={classes.cell}> {trade.side} </TableCell>
          <TableCell className={classes.cell}> {trade.pnl} </TableCell>
          <TableCell className={classes.cell}> {trade.calculated_comissions} </TableCell>
          <TableCell className={classes.cell}> {trade.net} </TableCell>
          <TableCell className={classes.cell}> {trade.trades_count} </TableCell>
          <TableCell className={classes.cell}> {trade.shares_traded} </TableCell>
        </TableRow>
      )});
      return(
        <TableContainer key={date} className={classes.tableContainer} component={Paper}>
        <Typography align={'center'} variant={'h5'}>{date} </Typography>
          <Table className={classes.table} size="small" aria-label="meal table">
            <TableHead>
              <TableRow>
                <TableCell size={"small"} className={classes.cellheaderTitle}> Ticker </TableCell>
                <TableCell size={"small"} className={classes.cellheaderTitle}> Side </TableCell>
                <TableCell size={"small"} className={classes.cellheaderTitle}> PNL </TableCell>
                <TableCell size={"small"} className={classes.cellheaderTitle}> Cal. Com. </TableCell>
                <TableCell size={"small"} className={classes.cellheaderTitle}> NET </TableCell>
                <TableCell size={"small"} className={classes.cellheaderTitle}> Trades </TableCell>
                <TableCell size={"small"} className={classes.cellheaderTitle}> Shares Traded </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {renderedTrades}
            </TableBody>
          </Table>
        </TableContainer>
      )
    });
  } else if (groupedFetchStatus === 'failed') {
    content = <div>there was an error Loading Trades</div>
  } else {
    content = <p>There are no saved trades </p>
  }


  return (
    <Grid container>
      <Grid item xs={1} />
      <Grid item xs={10}>
      {content}
      </Grid>
      <Grid item xs={1} />
    </Grid>
  )
}
