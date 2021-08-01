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
import TradeChartWrapper from '../charts/TradeChartWrapper';
import { timeParse } from "d3-time-format";
import { navbarSelected, selectActiveTab } from '../navbar/navBarSlicer'
import { selectUserIsLogedIn} from '../access/accessSlicer'


export default function TradeDetail(){
  const router = useRouter();
  const tradeSelected = useSelector(state => state.trades.tradeSelected);
  const dispatch = useDispatch();
  const {slug}  = router.query;
  const parseDate = timeParse("%H:%M:%S %Y/%m/%d");
  const tabSelected = useSelector(selectActiveTab);
  const userIsLogedIn = useSelector(selectUserIsLogedIn);


  useEffect(() => {
    if(tradeSelected == null){
      dispatch(fetchTrade(slug))
    }
    if(tabSelected != 1 && userIsLogedIn == true)
      dispatch(navbarSelected(1))
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
      <Grid container spacing={1}>
        <Grid item xs={1}>
        </Grid>
        <Grid item xs={10}>
          {tradeSelected
            ?
              <TradeChartWrapper uuid={tradeSelected.uuid} filledOrders={filledOrders} />
            :
              'No trade selected'}
        </Grid>
        <Grid item xs={1}>
        </Grid>
      </Grid>
    </div>
  )
}
