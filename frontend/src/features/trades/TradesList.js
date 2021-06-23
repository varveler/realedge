import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchTrades, selectAllTrades } from './tradesSlicer';
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
  cellheaderTitle: {
    textAlign: 'center',
    whiteSpace: 'nowrap'
  }
}));


export default function TradesList () {
  const userIsLogedIn = useSelector(selectUserIsLogedIn)
  const fetchTradesStatus = useSelector(state => state.trades.status);
  const trades = useSelector(selectAllTrades);
  const dispatch = useDispatch();
  const classes = useStyles();
  const router = useRouter()
  let content
  useEffect(() => {
    if (!userIsLogedIn) {
        router.push('/signin')
      } else {
        dispatch(navbarSelected(1))
        if (fetchTradesStatus === 'idle') {
          dispatch(fetchTrades())
        }
}
  }, [fetchTradesStatus, dispatch])


  if (fetchTradesStatus === 'loading') {
    content = <div className="loader">Loading Trades...</div>
  } else if (fetchTradesStatus === 'succeeded') {
    var dates = [];

    trades.map(trade => {
      let trimedDate = trade.start_time.split('T')[0]
      if(!dates.includes(trimedDate)){dates.push(trimedDate)}})
      var ordererByDayTrades = {}
      dates.forEach((date, i) => {
        var gs = trades.filter(trade => trade.start_time.split('T')[0] === date)
        ordererByDayTrades[date] = gs
    });
    content = dates.map((date, i) => {
      var slDate = date.replace(/-/g, '');
      var renderedTrades = ordererByDayTrades[date].map(trade => {
        return(
        <TableRow key={trade.uuid}>
          <TableCell className={classes.cell}>
            <Link href={`/trades/${trade.uuid}`}>{trade.ticker}</Link>
          </TableCell>
          <TableCell className={classes.cell}> {trade.start_time} </TableCell>
          <TableCell className={classes.cell}> {trade.end_time} </TableCell>
          <TableCell className={classes.cell}> {trade.duration} </TableCell>
          <TableCell className={classes.cell}> {trade.max_size} </TableCell>
          <TableCell className={classes.cell}> {trade.side} </TableCell>
          <TableCell className={classes.cell}> {trade.pnl} </TableCell>
          <TableCell className={classes.cell}> {trade.calculated_comissions} </TableCell>
          <TableCell className={classes.cell}> {trade.net} </TableCell>
          <TableCell className={classes.cell}> {trade.entries} </TableCell>
          <TableCell className={classes.cell}> {trade.exits} </TableCell>
          <TableCell className={classes.cell}> {trade.first_entry_price} </TableCell>
          <TableCell className={classes.cell}> {trade.last_exit_price} </TableCell>
          <TableCell className={classes.cell}> {trade.closed} </TableCell>
          <TableCell className={classes.cell}> {trade.position} </TableCell>
        </TableRow>
      )});
      return(
        <TableContainer key={date} className={classes.tableContainer} component={Paper}>
        <Typography align={'center'} variant={'h5'}>{date} </Typography>
          <Table className={classes.table} size="small" aria-label="meal table">
            <TableHead>
              <TableRow>
                <TableCell size={"small"} className={classes.cellheaderTitle}> Ticker </TableCell>
                <TableCell size={"small"} className={classes.cellheaderTitle}> Start Date </TableCell>
                <TableCell size={"small"} className={classes.cellheaderTitle}> End Date </TableCell>
                <TableCell size={"small"} className={classes.cellheaderTitle}> Duration </TableCell>
                <TableCell size={"small"} className={classes.cellheaderTitle}> Max Size </TableCell>
                <TableCell size={"small"} className={classes.cellheaderTitle}> Side </TableCell>
                <TableCell size={"small"} className={classes.cellheaderTitle}> PNL </TableCell>
                <TableCell size={"small"} className={classes.cellheaderTitle}> Cal. Com. </TableCell>
                <TableCell size={"small"} className={classes.cellheaderTitle}> NET </TableCell>
                <TableCell size={"small"} className={classes.cellheaderTitle}> Entries </TableCell>
                <TableCell size={"small"} className={classes.cellheaderTitle}> Exits </TableCell>
                <TableCell size={"small"} className={classes.cellheaderTitle}> FEP </TableCell>
                <TableCell size={"small"} className={classes.cellheaderTitle}> LEP </TableCell>
                <TableCell size={"small"} className={classes.cellheaderTitle}> Closed </TableCell>
                <TableCell size={"small"} className={classes.cellheaderTitle}> Position </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {renderedTrades}
            </TableBody>
          </Table>
        </TableContainer>
      )
    });
  } else if (fetchTradesStatus === 'failed') {
    content = <div>there was an error Loading Trades {error}</div>
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
