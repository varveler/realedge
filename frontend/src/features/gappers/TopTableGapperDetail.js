import React, {Fragment, useEffect} from 'react';
import { useSelector, useDispatch } from 'react-redux';
import Grid from '@material-ui/core/Grid';
import { makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';

const useStyles = makeStyles((theme) => ({
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
}));

export default function TopTableGapperDetail({gapper}){
  const classes = useStyles()

  return(
    <TableContainer className={classes.tableContainer} component={Paper}>
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
            <TableCell className={classes.cell}> {gapper.pm_s2_volume ? gapper.pm_s2_volume : 'N/A' } </TableCell>
            <TableCell className={classes.cell}> {gapper.pm_s1_market_cap ? gapper.pm_s1_market_cap : 'N/A' } </TableCell>
            <TableCell className={classes.cell}> {gapper.pm_s2_market_cap ? gapper.pm_s2_market_cap : 'N/A' } </TableCell>
            <TableCell className={classes.cell}> {gapper.pm_s1_float ? gapper.pm_s1_float : 'N/A' } </TableCell>
            <TableCell className={classes.cell}> {gapper.pm_s2_float ? gapper.pm_s2_float : 'N/A' } </TableCell>
            <TableCell className={classes.cell}> {gapper.pm_s1_held_percent_insiders ? gapper.pm_s1_held_percent_insiders : 'N/A' } </TableCell>
            <TableCell className={classes.cell}> {gapper.pm_s2_held_percent_insiders ? gapper.pm_s2_held_percent_insiders : 'N/A' } </TableCell>
            <TableCell className={classes.cell}> {gapper.pm_s1_held_percent_institutions ? gapper.pm_s1_held_percent_institutions : 'N/A' } </TableCell>
            <TableCell className={classes.cell}> {gapper.pm_s2_held_percent_institutions ? gapper.pm_s2_held_percent_institutions : 'N/A' } </TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </TableContainer>
  )
}
