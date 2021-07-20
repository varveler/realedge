import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchGappers, selectAllGappers } from './gappersSlicer';
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

//const useStyles = makeStyles((theme) => ({})


export default function TradeDetail(){

  const router = useRouter();
  console.log(router)
  const { id } = router.query;
  console.log(router.query)
  return(
    <div>
    Details
      {id}
    </div>
  )
}
