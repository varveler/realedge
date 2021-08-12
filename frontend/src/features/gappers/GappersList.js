import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchGappers, selectAllGappers, selectGapper, fetchMoreGappers, setDates, setisFetchingMore, setOldesDate } from './gappersSlicer';
import { selectUserIsLogedIn } from '../access/accessSlicer'
import Grid from '@material-ui/core/Grid';
import { makeStyles } from '@material-ui/core/styles';
import { navbarSelected } from '../navbar/navBarSlicer'
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import Link from 'next/link'
import { useRouter } from 'next/router'
import LinearProgress from '@material-ui/core/LinearProgress';

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
  cellTicker: {
    textAlign: 'center',
    cursor: 'pointer'
  },
  cellheaderTitle: {
    textAlign: 'center',
    whiteSpace: 'nowrap'
  }
}));


export default function GappersList () {
  const fetchGappersStatus = useSelector(state => state.gappers.status);
  const router = useRouter();
  const gappers = useSelector(selectAllGappers);
  const dispatch = useDispatch();
  const classes = useStyles();
  const userIsLogedIn = useSelector(selectUserIsLogedIn)
  const {dates, oldestDate, isFetchingMore} = useSelector(state => state.gappers);

  const handleRoute = (e, path, trade) => {
    e.preventDefault()
    dispatch(selectGapper(trade))
    router.push(path.pathname, `/gappers/${path.query.id}`, { shallow: true })
  }

  useEffect(() => {
    dispatch(navbarSelected(0))
    if (fetchGappersStatus === 'idle') {
      dispatch(fetchGappers())
    }
  }, [fetchGappersStatus, dispatch])

  useEffect(() => {
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  function handleScroll() {
    if (window.innerHeight + document.documentElement.scrollTop !== document.documentElement.offsetHeight) return;
      dispatch(setisFetchingMore(true))
  }

  useEffect(() => {
    if (!isFetchingMore) return;
    dispatch(fetchMoreGappers(oldestDate));
  }, [isFetchingMore,]);

  useEffect(() => {
    dispatch(setDates());
  }, [gappers]);

  useEffect(() => {
    dispatch(setOldesDate());
  }, [dates]);

  let content
  const renderRowTableUserIsLogedIn = (gapper, id) => (
    <TableRow key={id}>
      <TableCell onClick={ (e) => handleRoute(e, {pathname: '/gappers/[id]', query: { id: id }}, {date: gapper.date, ticker: gapper.ticker})} //todo refactor
                className={classes.cellTicker}>
        <a>{gapper.ticker}</a>
      </TableCell>
      <TableCell className={classes.cell}> {gapper.last} </TableCell>
      <TableCell className={classes.cell}> {gapper.gap_percentage_display} </TableCell>
      <TableCell className={classes.cell}> {gapper.pm_s2_volume} </TableCell>
      <TableCell className={classes.cell}> {gapper.pm_s1_market_cap} </TableCell>
      <TableCell className={classes.cell}> {gapper.pm_s2_market_cap} </TableCell>
      <TableCell className={classes.cell}> {gapper.pm_s1_float} </TableCell>
      <TableCell className={classes.cell}> {gapper.pm_s2_float} </TableCell>
      <TableCell className={classes.cell}> {gapper.pm_s1_held_percent_insiders} </TableCell>
      <TableCell className={classes.cell}> {gapper.pm_s2_held_percent_insiders} </TableCell>
      <TableCell className={classes.cell}> {gapper.pm_s1_held_percent_institutions} </TableCell>
      <TableCell className={classes.cell}> {gapper.pm_s2_held_percent_institutions} </TableCell>
      <TableCell className={classes.cell}> {gapper.pm_s1_short_percent_float} </TableCell>
      <TableCell className={classes.cell}> {gapper.pm_red_gaps} </TableCell>
      <TableCell className={classes.cell}> {gapper.pm_observations} </TableCell>
    </TableRow>
  )
  const renderRowTableUserNotLogedIn = (gapper, id) => (
    <TableRow key={id}>
      <TableCell onClick={ (e) => handleRoute(e, {pathname: '/gappers/[id]', query: { id: id }}, {date: gapper.date, ticker: gapper.ticker})} //todo refactor
                className={classes.cellTicker}>
        <a>{gapper.ticker}</a>
      </TableCell>
      <TableCell className={classes.cell}> {gapper.last} </TableCell>
      <TableCell className={classes.cell}> {gapper.gap_percentage_display} </TableCell>
      <TableCell className={classes.cell}> {gapper.pm_s2_volume} </TableCell>
      <TableCell className={classes.cell}> {gapper.pm_s1_market_cap} </TableCell>
    </TableRow>
  )
  const renderHeadersUserIsLogedIn = () => (
    <TableHead>
      <TableRow>
        <TableCell size={"small"} className={classes.cellheaderTitle}> Ticker </TableCell>
        <TableCell size={"small"} className={classes.cellheaderTitle}> Price </TableCell>
        <TableCell size={"small"} className={classes.cellheaderTitle}> Gap % </TableCell>
        <TableCell size={"small"} className={classes.cellheaderTitle}> Volume </TableCell>
        <TableCell size={"small"} className={classes.cellheaderTitle} colSpan={2}>Market Capitalization </TableCell>
        <TableCell size={"small"} className={classes.cellheaderTitle} colSpan={2}>Float Shares</TableCell>
        <TableCell size={"small"} className={classes.cellheaderTitle} colSpan={2}>Held by Insiders </TableCell>
        <TableCell size={"small"} className={classes.cellheaderTitle} colSpan={2}>Held by Institutions </TableCell>
        <TableCell size={"small"} className={classes.cellheaderTitle}> Short % Float </TableCell>
        <TableCell size={"small"} className={classes.cellheaderTitle}> RGP% </TableCell>
        <TableCell size={"small"} className={classes.cellheaderTitle}> # OBS </TableCell>
      </TableRow>
    </TableHead>
  )
  const renderHeadersUserNotLogedIn = () => (
    <TableHead>
      <TableRow>
        <TableCell size={"small"} className={classes.cellheaderTitle}> Ticker </TableCell>
        <TableCell size={"small"} className={classes.cellheaderTitle}> Price </TableCell>
        <TableCell size={"small"} className={classes.cellheaderTitle}> Gap % </TableCell>
        <TableCell size={"small"} className={classes.cellheaderTitle}> Volume </TableCell>
        <TableCell size={"small"} className={classes.cellheaderTitle} colSpan={2}>Market Cap. </TableCell>
      </TableRow>
    </TableHead>
  )


  if (fetchGappersStatus === 'loading') {
    content = <div className="loader">Loading...</div>
  } else if (gappers.length > 1 ) {
    var row = userIsLogedIn ? renderRowTableUserIsLogedIn : renderRowTableUserNotLogedIn;
    var headers = userIsLogedIn ? renderHeadersUserIsLogedIn : renderHeadersUserNotLogedIn;
    var ordererByDayGappers = {}
    dates.forEach((date, i) => {
      var gs = gappers.filter(gapper => gapper.date === date)
      ordererByDayGappers[date] = gs
    });
    content = dates.map((date, i) => {
      var slDate = date.replace(/-/g, '');
      var renderedGappers = ordererByDayGappers[date].map(gapper => {
        var id = `${gapper.ticker}-${slDate}`;
        return(
          row(gapper, id)
      )});
      return(
        <TableContainer key={date} className={classes.tableContainer} component={Paper}>
        <Typography align={'center'} variant={'h5'}>{date} </Typography>
          <Table className={classes.table} size="small" aria-label="table">
            {headers()}
            <TableBody>
              {renderedGappers}
            </TableBody>
          </Table>
        </TableContainer>
      )
    });
  } else  {
    content = <div>there was an error </div>
  }


  return (
    <Grid container>
      <Grid item xs={userIsLogedIn ? 1 : 3} />
      <Grid item xs={userIsLogedIn ? 10 : 6}>
      {content}
      <br/>
      <br/>
      <LinearProgress/>
      <br/>
      <br/>
      </Grid>
      <Grid item xs={userIsLogedIn ? 1 : 3} />
    </Grid>
  )
}
