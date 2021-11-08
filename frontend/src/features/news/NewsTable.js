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
import {fetchNews} from './newsSlicer'
import { selectUserIsLogedIn} from '../access/accessSlicer'
import { timeFormat } from "d3-time-format";
import {dateTimeFromStrToFormatedStr} from '../../components/helpers'

const useStyles = makeStyles((theme) => ({
  groupedTradesDetailContainer:{
    marginTop: '10px'
  },
  bar: {
    color:'pink',
    borderBottom: '1px solid gray'
  },
  tradesTableContainer: {
    marginLeft:'0px'
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
    textAlign:'center'
  },
  cellTrade: {
    textAlign:'center',
    whiteSpace: 'nowrap'
  },
  cellTitle: {
    textAlign:'left',
    whiteSpace: 'nowrap'
  },
  tradesDetailsTitle:{
    fontSize: '20px'
  },
  cellLink:{
  color:'#556CD6'
  },
  infoDate:{
    color: 'gray',
    marginLeft: '7px'
  },
  infoTitle:{
    color: 'gray',
    fontSize: '1rem',
    paddingBottom:'10px'
  },
  table:{
    paddingTop:'10px'
  }
}));

export default function TradesDetails({news, _from, to, ticker}){
  const classes = useStyles()
  const userIsLogedIn = useSelector(selectUserIsLogedIn)
  const formatTime = timeFormat("%Y %m %d %H:%M")
  return(
    <Fragment>
      <div className={classes.mainTradesContainer}>
          <TableContainer className={classes.tradesTableContainer}>
          <Typography className={classes.infoTitle} align='center' component='p'>
            { _from ? `${ticker} news from
              ${_from.substr(4,2)}/${_from.substr(6,2)}/${_from.substr(0,4)}
              to
              ${to.substr(4,2)}/${to.substr(6,2)}/${to.substr(0,4)}`
            : null}
          </Typography>
            <Table className={classes.table} size="small" aria-label="table">
              <TableBody>
                {news && news.length >= 1 && news.map(n => (
              <TableRow key={n.uuid}>
                <TableCell size={"small"} className={classes.cellTrade}> {dateTimeFromStrToFormatedStr(n.publish_date)} <span className={classes.infoDate}>{n.natural_time}</span>  </TableCell>
                <TableCell size={"small"} className={classes.cellTitle}> <a className={classes.cellLink} href={n.url } target='_blank'> {n.short_title} </a> </TableCell>
                <TableCell size={"small"} className={classes.cellTitle}> {n.source} </TableCell>
                {userIsLogedIn ?
                <TableCell size={"small"} className={classes.cellTrade}> {n.internal_source} </TableCell>
                : null}
              </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </div>
    </Fragment>
  )
}
