import React, {Fragment, useEffect} from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
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

export default function TradesDetails({news}){
  const classes = useStyles()

  return(
    <Fragment>
      <div className={classes.mainTradesContainer}>
        <Typography align={'center'} className={classes.tradesDetailsTitle}> News </Typography>
          <TableContainer className={classes.tradesTableContainer}>
            <Table className={classes.table} size="small" aria-label="table">
              <TableHead>
                <TableRow>
                  <TableCell size={"small"} className={classes.cellheaderTradeTitle}> Date </TableCell>
                  <TableCell size={"small"} className={classes.cellheaderTradeTitle}> Title </TableCell>
                  <TableCell size={"small"} className={classes.cellheaderTradeTitle}> Source </TableCell>
                  <TableCell size={"small"} className={classes.cellheaderTradeTitle}> Internal Source </TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {news && news.length >= 1 && news.map(n => (
              <TableRow key={n.uuid}>
                <TableCell className={classes.cellTrade}> {n.publish_date} </TableCell>
                <TableCell className={classes.cellTrade}> {n.title} </TableCell>
                <TableCell className={classes.cellTrade}> {n.source} </TableCell>
                <TableCell className={classes.cellTrade}> {n.internal_source} </TableCell>
              </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </div>
    </Fragment>
  )
}
