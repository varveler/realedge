import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchTrade } from './tradesSlicer';
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
import ChartWrapper from '../charts/ChartWrapper';
import { timeParse } from "d3-time-format";



export default function GapperDetail(){
  const router = useRouter();
  const tradeSelected = useSelector(state => state.trades.tradeSelected)
  const dispatch = useDispatch();
  const {slug}  = router.query;
  const parseDate = timeParse("%H:%M:%S %Y/%m/%d");
  useEffect(() => {
    if(tradeSelected == null){
      console.log('slug is', slug)
      console.log('ts', tradeSelected)
      dispatch(fetchTrade(slug))
  }
  })
  const filledOrders = tradeSelected ? tradeSelected.orders.filter(
    order => order.status === "FI").map(
    order => {
              let parsedDate = parseDate(order.last_time)
              const norder = {...order, date: parsedDate, price: parseFloat(order.price)}
              return norder
    }
  )
 : []
  return(
    <div>
      {tradeSelected
        ?
          <ChartWrapper uuid={tradeSelected.uuid} filledOrders={filledOrders} />
        :
          'No trade selected'}
    </div>
  )
}
