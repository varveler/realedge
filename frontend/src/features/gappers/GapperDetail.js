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
  }
}))

export default function GapperDetail(){

  const router = useRouter();
  const { id } = router.query;
  const classes = useStyles();
  const dispatch = useDispatch()
  const userIsLogedIn = useSelector(selectUserIsLogedIn)
  const gapperSelected = useSelector(state => state.gappers.gapperSelected)
  const gapperSelectedStatus = useSelector(state => state.gappers.gapperSelectedStatus)
  useEffect(() => {
    if(gapperSelected == null) {
      dispatch(fetchGapper(id))
    }
  })
  if(gapperSelected === null) return <p> Loading gapper .... </p>
  return(
<div>
        {gapperSelected ?
        <div>
          <Grid container spacing={1}>
            <Grid item xs={2}>
            </Grid>
            <Grid item xs={8}>
                  <Grid container spacing={1}>
                    <Grid item xs={3}>
                      <Typography className={classes.ticker} component='h1'>{gapperSelected.ticker}</Typography>
                      <Typography className={classes.info} component='p'>{gapperSelected.company_name}</Typography>
                      { gapperSelected.industry ? <Typography className={classes.info} component='p'><span className={classes.infoTitle}>Industry:</span> {gapperSelected.industry}</Typography>:null}
                      <Typography className={ classes.percentage} component='p'> {gapperSelected.gap_percentage_display}<span className={classes.infoTitle}>{' '}gap</span></Typography>
                    </Grid>
                    <Grid item xs={9}>
                      <TableContainer key={id} className={classes.tableContainer} component={Paper}>
                        <Table className={classes.table} size="small" aria-label="table">
                          <TableHead>
                            <TableRow>
                              <TableCell size={"small"} className={classes.cellheaderTitle}> PM Volume </TableCell>
                              <TableCell size={"small"} className={classes.cellheaderTitle} colSpan={2}>Market Capitalization </TableCell>
                              <TableCell size={"small"} className={classes.cellheaderTitle} colSpan={2}>Float Shares</TableCell>
                              <TableCell size={"small"} className={classes.cellheaderTitle} colSpan={2}>Held by Insiders </TableCell>
                              <TableCell size={"small"} className={classes.cellheaderTitle} colSpan={2}>Held by Institutions </TableCell>
                            </TableRow>
                          </TableHead>
                          <TableBody>
                            <TableRow>
                              <TableCell className={classes.cell}> {gapperSelected.pm_s2_volume} </TableCell>
                              <TableCell className={classes.cell}> {gapperSelected.pm_s1_market_cap} </TableCell>
                              <TableCell className={classes.cell}> {gapperSelected.pm_s2_market_cap} </TableCell>
                              <TableCell className={classes.cell}> {gapperSelected.pm_s1_float} </TableCell>
                              <TableCell className={classes.cell}> {gapperSelected.pm_s2_float} </TableCell>
                              <TableCell className={classes.cell}> {gapperSelected.pm_s1_held_percent_insiders} </TableCell>
                              <TableCell className={classes.cell}> {gapperSelected.pm_s2_held_percent_insiders} </TableCell>
                              <TableCell className={classes.cell}> {gapperSelected.pm_s1_held_percent_institutions} </TableCell>
                              <TableCell className={classes.cell}> {gapperSelected.pm_s2_held_percent_institutions} </TableCell>
                            </TableRow>
                          </TableBody>
                        </Table>
                      </TableContainer>
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
                {gapperSelected ? <GapperChartWrapper slug={id} /> : <p>no gapper slected</p> }
            </Grid>
            <Grid item xs={2}>
            </Grid>
          </Grid>
      </div>
      : <p> No gapper selected </p>}
    </div>

  )
}
