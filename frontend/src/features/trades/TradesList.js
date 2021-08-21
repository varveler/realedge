import React, {Fragment} from 'react';
import { useSelector, useDispatch } from 'react-redux';
import Grid from '@material-ui/core/Grid';
import { makeStyles } from '@material-ui/core/styles';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Switch from '@material-ui/core/Switch';
import Box from '@material-ui/core/Box';
import {handleChangeGroupByTicker} from '../access/accessSlicer';
import ByDayByTicker from './ListByDayByTicker';
import ByDayByTrade from './ListByDayByTrade';


const useStyles = makeStyles((theme) => ({
  bar: {
    color:'pink',
    borderBottom: '1px solid gray'
}
}));


export default function TradesList(){
  const classes = useStyles();
  const dispatch = useDispatch();
  const groupByTicker = useSelector(state => state.access.groupByTicker )
  const handleChange = () => {
    dispatch(handleChangeGroupByTicker())
  }
  return (
  <Fragment>
    <Grid container className={classes.bar}>
      <Grid item xs={3} />
      <Grid item xs={6}>
        <Box display="flex" justifyContent="flex-end" >
          <Box>
            <FormGroup row>
              <FormControlLabel
                control={<Switch checked={groupByTicker} onChange={handleChange} name="checkedGroupByTicker" />}
                label="Group Trades by Ticker"
              />
            </FormGroup>
          </Box>
        </Box>
      </Grid>
      <Grid item xs={3} />
    </Grid>
    {groupByTicker ? <ByDayByTicker/> : <ByDayByTrade/> }
  </Fragment>
  )
}
