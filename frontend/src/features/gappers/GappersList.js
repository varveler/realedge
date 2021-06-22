import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchGappers, selectAllGappers } from './gappersSlicer';
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
  cellheaderTitle: {
    textAlign: 'center',
    whiteSpace: 'nowrap'
  }
}));


export default function GappersList () {
  const fetchGappersStatus = useSelector(state => state.gappers.status);
  const gappers = useSelector(selectAllGappers);
  const dispatch = useDispatch();
  const classes = useStyles();
  let content
  useEffect(() => {
    dispatch(navbarSelected(0))
    if (fetchGappersStatus === 'idle') {
      console.log('env', process.env.NEXT_PUBLIC_API_URL)
      dispatch(fetchGappers())
    }
  }, [fetchGappersStatus, dispatch])
  console.log(gappers)

  if (fetchGappersStatus === 'loading') {
    content = <div className="loader">Loading...</div>
  } else if (fetchGappersStatus === 'succeeded') {
    var dates = [];

    gappers.map(gapper => {if(!dates.includes(gapper.date)){dates.push(gapper.date)}})
    var ordererByDayGappers = {}
    dates.forEach((date, i) => {
      var gs = gappers.filter(gapper => gapper.date === date)
      ordererByDayGappers[date] = gs
    });
    console.log(dates)
    console.log(ordererByDayGappers)
    content = dates.map((date, i) => {
      console.log(ordererByDayGappers[date])
      var slDate = date.replace(/-/g, '');
      var renderedGappers = ordererByDayGappers[date].map(gapper => {
        var id = `${gapper.ticker}-${slDate}`;
        return(
        <TableRow key={id}>
          <TableCell className={classes.cell}>
            <Link href={`/gappers/${id}`}>{gapper.ticker}</Link>
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
      )});
      console.log(renderedGappers)
      return(
        <TableContainer key={date} className={classes.tableContainer} component={Paper}>
        <Typography align={'center'} variant={'h5'}>{date} </Typography>
          <Table className={classes.table} size="small" aria-label="meal table">
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
            <TableBody>
              {renderedGappers}
            </TableBody>
          </Table>
        </TableContainer>
      )
    });
  } else if (fetchGappersStatus === 'failed') {
    content = <div>there was this error_{error}</div>
  }


  return (
    <Grid container>
      <Grid item xs={1} />
      <Grid item xs={10}>
      {content}
      </Grid>
      <Grid item xs={1} />
    </Grid>
  )
}
