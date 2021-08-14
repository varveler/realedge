import React from 'react';
import Grid from '@material-ui/core/Grid';
import { makeStyles } from '@material-ui/core/styles';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Switch from '@material-ui/core/Switch';

const useStyles = makeStyles((theme) => ({
  x:{color:'pink'}
}));


export default function TradesList(){

  return (
    <Grid container>
      <Grid item xs={3} />
      <Grid item xs={6}>
        <FormGroup row>
          <FormControlLabel
            control={<Switch checked={true} onChange={console.log('changed')} name="checkedGroupByTicker" />}
            label="Group Trades by Ticker"
          />
        </FormGroup>
      </Grid>
      <Grid item xs={3} />
    </Grid>
  )
}
