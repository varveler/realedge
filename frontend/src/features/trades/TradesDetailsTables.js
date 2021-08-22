import React, {Fragment, useEffect} from 'react';
import { useSelector, useDispatch } from 'react-redux';
import Grid from '@material-ui/core/Grid';
import { makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Typography from '@material-ui/core/Typography';


const useStyles = makeStyles((theme) => ({
  groupedTradesDetailContainer:{
    marginTop: '10px'
  },
  bar: {
    color:'pink',
    borderBottom: '1px solid gray'
  },
  tradesTableContainer: {
    marginLeft:'30px'
  },
  mainTradesContainer:{
    marginTop: '20px'
  },
  cellheaderTitleGroupedDetails:{
    fontSize:'20px',
      textAlign:'center'
  },
  cellGroupedDetails:{
    fontSize: '18px',
    textAlign:'center'
  },
  cellheaderTradeTitle: {
    fontSize: '18px',
    textAlign:'center'
  },
  cellTrade: {
    fontSize: '16px',
    textAlign:'center'
  },
  tradesDetailsTitle:{
    fontSize: '20px'
  },
}));

export default function TradesDetails({groupedTradesDetails, trades, orders}){
  const classes = useStyles()

  return(
    <Fragment>
    {groupedTradesDetails ?
      <div className={classes.groupedTradesDetailContainer}>
      <TableContainer key={groupedTradesDetails.date} className={classes.tableContainer}>
        <Table className={classes.table} size="small" aria-label="meal table">
          <TableHead>
            <TableRow>
              <TableCell size={"small"} className={classes.cellheaderTitleGroupedDetails}> Ticker </TableCell>
              <TableCell size={"small"} className={classes.cellheaderTitleGroupedDetails}> Side </TableCell>
              <TableCell size={"small"} className={classes.cellheaderTitleGroupedDetails}> PNL </TableCell>
              <TableCell size={"small"} className={classes.cellheaderTitleGroupedDetails}> Cal. Com. </TableCell>
              <TableCell size={"small"} className={classes.cellheaderTitleGroupedDetails}> NET </TableCell>
              <TableCell size={"small"} className={classes.cellheaderTitleGroupedDetails}> Trades </TableCell>
              <TableCell size={"small"} className={classes.cellheaderTitleGroupedDetails}> Shares Traded </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
          <TableRow key={groupedTradesDetails.uuid}>
            <TableCell className={classes.cellGroupedDetails}> {groupedTradesDetails.ticker} </TableCell>
            <TableCell className={classes.cellGroupedDetails}> {groupedTradesDetails.side} </TableCell>
            <TableCell className={classes.cellGroupedDetails}> {groupedTradesDetails.pnl} </TableCell>
            <TableCell className={classes.cellGroupedDetails}> {groupedTradesDetails.calculated_comissions} </TableCell>
            <TableCell className={classes.cellGroupedDetails}> {groupedTradesDetails.net} </TableCell>
            <TableCell className={classes.cellGroupedDetails}> {groupedTradesDetails.trades_count} </TableCell>
            <TableCell className={classes.cellGroupedDetails}> {groupedTradesDetails.shares_traded} </TableCell>
          </TableRow>
          </TableBody>
        </Table>
      </TableContainer>
    </div>
    : null}
    <div className={classes.mainTradesContainer}>
      <Typography align={'center'} className={classes.tradesDetailsTitle}> {trades && trades.length == 1 ? 'Trade Details' : 'Trades Details' } </Typography>
        <TableContainer className={classes.tradesTableContainer}>
          <Table className={classes.table} size="small" aria-label="table">
            <TableHead>
              <TableRow>
                <TableCell size={"small"} className={classes.cellheaderTradeTitle}> Side </TableCell>
                <TableCell size={"small"} className={classes.cellheaderTradeTitle}> Start Date </TableCell>
                <TableCell size={"small"} className={classes.cellheaderTradeTitle}> End Date </TableCell>
                <TableCell size={"small"} className={classes.cellheaderTradeTitle}> Duration </TableCell>
                <TableCell size={"small"} className={classes.cellheaderTradeTitle}> Max Size </TableCell>
                <TableCell size={"small"} className={classes.cellheaderTradeTitle}> PNL </TableCell>
                <TableCell size={"small"} className={classes.cellheaderTradeTitle}> Cal. Com. </TableCell>
                <TableCell size={"small"} className={classes.cellheaderTradeTitle}> NET </TableCell>
                <TableCell size={"small"} className={classes.cellheaderTradeTitle}> Entries </TableCell>
                <TableCell size={"small"} className={classes.cellheaderTradeTitle}> Exits </TableCell>
                <TableCell size={"small"} className={classes.cellheaderTradeTitle}> Orders </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {trades && trades.length >= 1 && trades.map(trade => {
              const ordersTrade = [];
              return(
              <TableRow key={trade.uuid}>
                <TableCell className={classes.cellTrade}> {trade.side == 'SH' ? 'Short' : 'Long'} </TableCell>
                <TableCell className={classes.cellTrade}> {trade.start_time} </TableCell>
                <TableCell className={classes.cellTrade}> {trade.end_time} </TableCell>
                <TableCell className={classes.cellTrade}> {trade.duration} </TableCell>
                <TableCell className={classes.cellTrade}> {trade.max_size} </TableCell>
                <TableCell className={classes.cellTrade}> {trade.pnl} </TableCell>
                <TableCell className={classes.cellTrade}> {trade.calculated_comissions} </TableCell>
                <TableCell className={classes.cellTrade}> {trade.net} </TableCell>
                <TableCell className={classes.cellTrade}> {trade.entries} </TableCell>
                <TableCell className={classes.cellTrade}> {trade.exits} </TableCell>
                <TableCell className={classes.cellTrade}> show </TableCell>
              </TableRow>
              )
              })}
            </TableBody>
          </Table>
        </TableContainer>
      </div>
    </Fragment>
  )
}
