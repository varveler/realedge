import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchTrade, submitComment, changeComment } from './tradesSlicer';
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
import { fetchBarsTrade, setFetchChartStatus } from '../charts/chartsSlicer';

const useStyles = makeStyles((theme) => ({
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
  const tradeSelected = useSelector(state => state.trades.tradeSelected);
  const dispatch = useDispatch();
  const {slug}  = router.query;
  const parseDate = timeParse("%H:%M:%S %Y/%m/%d");
  const tabSelected = useSelector(selectActiveTab);
  const userIsLogedIn = useSelector(selectUserIsLogedIn);
  const chartData = useSelector(state => state.charts.data)
  const fetchChartStatus = useSelector(state => state.charts.status)


  useEffect(() => {
    if(tradeSelected == undefined){
      dispatch(fetchTrade(slug))
    }
    if(tabSelected != 1 && userIsLogedIn == true)
      dispatch(navbarSelected(1))
    return function cleanup() {
      dispatch(setFetchChartStatus('idle'))
    };

  },[])
  const filledOrders = tradeSelected ? tradeSelected.orders.filter(
    order => order.status === "FI").map(
      order => {
                let parsedDate = parseDate(order.last_time)
                const norder = {...order, date: parsedDate, price: parseFloat(order.price)}
                return norder
      }
    )
  : []
  if(tradeSelected && fetchChartStatus == 'idle' ){
    dispatch(fetchBarsTrade({uuid:tradeSelected.uuid}))
  }
  const renderTradeDetails = (tradeSelected) => (
    <div>
      <Grid container spacing={1}>
        <Grid item xs={2}>
        </Grid>
        <Grid item xs={8}>
            <Grid container spacing={1}>
              <Grid item xs={3}>
                {tradeSelected.pnl > 0 ?
                  <Typography className={classes.profit} component='h1'>{tradeSelected.pnl}<span className={classes.infoTitle}>{' '}profit</span></Typography>
                : <Typography className={classes.loss} component='h1'>{tradeSelected.pnl}<span className={classes.infoTitle}>{' '}loss</span></Typography>
                }
                <Typography className={classes.info} component='p'><span className={classes.infoTitle}>on{' '}</span>{tradeSelected.ticker} <span className={classes.infoTitle}>{' '}{tradeSelected.natural_time}</span></Typography>
              </Grid>
              <Grid item xs={9}>
                <TableContainer className={classes.tableContainer} component={Paper}>
                  <Table className={classes.table} size="small" aria-label="table">
                    <TableHead>
                      <TableRow>
                        <TableCell size={"small"} className={classes.cellheaderTitle}> PM Volume </TableCell>
                        <TableCell size={"small"} className={classes.cellheaderTitle} colSpan={2}>Market Capitalization </TableCell>
                        <TableCell size={"small"} className={classes.cellheaderTitle} colSpan={2}>Float Shares</TableCell>
                        <TableCell size={"small"} className={classes.cellheaderTitle} colSpan={2}>Held by Insiders </TableCell>
                        <TableCell size={"small"} className={classes.cellheaderTitle} colSpan={2}>Held by Institutions </TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      <TableRow>
                        {/* }<TableCell className={classes.cell}> {gapper.pm_s2_volume} </TableCell>
                        <TableCell className={classes.cell}> {gapper.pm_s1_market_cap} </TableCell>
                        <TableCell className={classes.cell}> {gapper.pm_s2_market_cap} </TableCell>
                        <TableCell className={classes.cell}> {gapper.pm_s1_float} </TableCell>
                        <TableCell className={classes.cell}> {gapper.pm_s2_float} </TableCell>
                        <TableCell className={classes.cell}> {gapper.pm_s1_held_percent_insiders} </TableCell>
                        <TableCell className={classes.cell}> {gapper.pm_s2_held_percent_insiders} </TableCell>
                        <TableCell className={classes.cell}> {gapper.pm_s1_held_percent_institutions} </TableCell>
                        <TableCell className={classes.cell}> {gapper.pm_s2_held_percent_institutions} </TableCell> */}
                      </TableRow>
                    </TableBody>
                  </Table>
                </TableContainer>
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
          <TradeChartWrapper uuid={tradeSelected.uuid} filledOrders={filledOrders} data={chartData}/>
          <TextField
            className={classes.tradeComents}
            id="outlined-multiline-static"
            label="Trade Comments"
            fullWidth
            multiline
            rows={4}
            variant="outlined"
            value={tradeSelected.comments}
            onChange={event => dispatch(changeComment(event.target.value))}
          />
          <Button onClick={(event) => {event.preventDefault; dispatch(submitComment({uuid:tradeSelected.uuid, comment:tradeSelected.comments}))}} variant="contained" color="primary">
            Save
          </Button>
        </Grid>
        <Grid item xs={1}>
        </Grid>
      </Grid>
    </div>
  )
  const renderNoTradeSelected = () => <p> Loading Trade Data.... </p>

  return(
    <div>
      {tradeSelected ? renderTradeDetails(tradeSelected) : renderNoTradeSelected}
    </div>
  )
}
