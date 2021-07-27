import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchGappers, selectAllGappers, fetchGapper } from './gappersSlicer';
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
import { selectUserIsLogedIn} from '../access/accessSlicer'
import GapperChartWrapper from '../charts/GapperChartWrapper'

//const useStyles = makeStyles((theme) => ({})

const useStyles = makeStyles((theme) => {
  root:{

  }

})

export default function TradeDetail(){

  const router = useRouter();
  const { id } = router.query;
  const classes = useStyles();
  const dispatch = useDispatch()
  const userIsLogedIn = useSelector(selectUserIsLogedIn)
  const gapperSelected = useSelector(state => state.gappers.gapperSelected)
  const gapperSelectedStatus = useSelector(state => state.gappers.gapperSelectedStatus)
  console.log('id', id)

  useEffect(() => {
    if(gapperSelected == null) {
      console.log('runnng fetch gapper', id)
      dispatch(fetchGapper(id))
    }
  })
  return(
      <div>
        { userIsLogedIn ?
          <Grid container spacing={1}>
            <Grid item xs={2}>
            </Grid>
            <Grid item xs={8}>
              {gapperSelected
                ?
                  <GapperChartWrapper slug={id} />
                :
                  'No trade selected'}
            </Grid>
            <Grid item xs={2}>
            </Grid>
          </Grid>
        :
          <p>Please Login to see this page</p>
        }
      </div>
  )
}
