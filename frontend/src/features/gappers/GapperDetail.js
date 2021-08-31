import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchGappers, selectAllGappers, fetchGapper } from './gappersSlicer';
import Grid from '@material-ui/core/Grid';
import { makeStyles } from '@material-ui/core/styles';
import TableContainer from '@material-ui/core/TableContainer';
import Table from '@material-ui/core/Table';
import TableHead from '@material-ui/core/TableHead';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import { useRouter } from 'next/router'
import { selectUserIsLogedIn} from '../access/accessSlicer'
import GapperChartWrapper from '../charts/GapperChartWrapper'
import {fetchBarsGapper, setFetchChartStatus, setFromTo} from '../charts/chartsSlicer'
import NewsTable from '../news/NewsTable'
import {fetchNews} from '../news/newsSlicer'
import { timeFormat } from "d3-time-format";
import {fromToDates} from '../../components/helpers'
import TopTableGapperDetail from './TopTableGapperDetail'

//const useStyles = makeStyles((theme) => ({})

const useStyles = makeStyles((theme) => ({
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
  gapperContainer:{
  paddingTop: '30px'
  }
}))


export default function GapperDetail(){

  const router = useRouter();
  const { id } = router.query;
  const classes = useStyles();
  const dispatch = useDispatch()
  const userIsLogedIn = useSelector(selectUserIsLogedIn)
  const selectedGapper = useSelector(state => state.gappers.selected)
  const gapperSelectedStatus = useSelector(state => state.gappers.gapperSelectedStatus)
  const chartData = useSelector(state => state.charts.data)
  const fetchChartStatus = useSelector(state => state.charts.status)
  const {news, newsStatus} = useSelector(state => state.news)
  const {_from, to} = useSelector(state => state.charts)
  console.log(id, _from, to)
  useEffect(() => {
    return function cleanup() {
      dispatch(setFetchChartStatus('idle'))
    };
  },[])
  useEffect(() => {
    if(id != undefined) {
      dispatch(fetchGapper(id))
      var {from, to} = fromToDates(id.split('-')[1])
      console.log('id.split', id.split('-')[1])
      console.log(from,to)
      dispatch(setFromTo({_from: from, to: to}))
      if(fetchChartStatus == 'idle') dispatch(fetchBarsGapper({slug: id}))
    }
  },[id])

  useEffect(() => {
    if(id != undefined && _from != undefined && to != undefined) {
    dispatch(fetchNews({ticker: id.split('-')[0], from:_from, to:to}))
    }
  },[id, _from, to])
  if(selectedGapper === undefined) return <p> Loading.... </p>
  return(
<div>
        {selectedGapper ?
        <div className={classes.gapperContainer}>
          <Grid container spacing={1}>
            <Grid item xs={2}>
            </Grid>
            <Grid item xs={8}>
                  <Grid container spacing={1}>
                    <Grid item xs={3}>
                      <Typography className={classes.ticker} component='h1'>{selectedGapper.ticker}</Typography>
                      <Typography className={classes.info} component='p'>{selectedGapper.company_name}</Typography>
                      { selectedGapper.industry ? <Typography className={classes.info} component='p'><span className={classes.infoTitle}>Industry:</span> {selectedGapper.industry}</Typography>:null}
                      <Typography className={ classes.percentage} component='p'> {selectedGapper.gap_percentage_display}<span className={classes.infoTitle}>{' '}gap</span></Typography>
                    </Grid>
                    <Grid item xs={9}>
                      <TopTableGapperDetail gapper={selectedGapper} />
                    </Grid>
                  </Grid>
            </Grid>
            <Grid item xs={2}>
            </Grid>
          </Grid>
          <Grid container spacing={1}>
            <Grid item xs={2}>
            </Grid>
            <Grid item xs={8}>
                {selectedGapper ? <GapperChartWrapper slug={id} data={chartData} /> : <p>no gapper slected</p> }
                {news && news.length >= 1 ? <NewsTable news={news} /> : <Typography className={classes.infoTitle} align={'center'} component='p'>No news found</Typography> }
            </Grid>
            <Grid item xs={2}>
            </Grid>
          </Grid>
      </div>
      : <p> No gapper selected </p>}
    </div>

  )
}
