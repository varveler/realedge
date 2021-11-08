import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';
import Button from  '@material-ui/core/Button';
import {changeComments, getLogs, submitLogs, deleteLogs } from './logsSlicer';


const useStyles = makeStyles((theme) => ({
  containerComments:{
    marginTop: '20px'
  },
  tradeComents: {
    marginTop: '25px'
  },
  button:{
    margin: '5px'
  }
}))

export default function CommentsForm({ticker, date}){
  const classes = useStyles();
  const dispatch = useDispatch();
  const {comments, bufferComments, uuid, getCommentsStatus }  = useSelector(state => state.logs)


  useEffect(() => {
    if(getCommentsStatus === 'idle' && ticker != undefined && date != undefined){
      dispatch(getLogs({ticker, date}))
    }
  },[])

  useEffect(() => {
    if(comments != undefined){dispatch(changeComments(comments))}
  },[comments])

  const handleSubmit = (uuid, bufferComments, ticker, date) => {
    if(bufferComments==''){
      dispatch(deleteLogs({uuid:uuid, comments:bufferComments, ticker:ticker, date:date}))
    }else{
      dispatch(submitLogs({uuid:uuid, comments:bufferComments, ticker:ticker, date:date}))
    }
  }

  return (
    <div className={classes.containerComments}>
      <Grid container spacing={1}>
        <Grid item xs={12} justify="space-between">
          <TextField
            className={classes.tradeComents}
            id="outlined-multiline-static"
            label="Trade Comments"
            fullWidth
            multiline
            rows={4}
            variant="outlined"
            value={bufferComments || ''}
            onChange={event => dispatch(changeComments(event.target.value))}
          />
          <Button className={classes.button}
                  onClick={(event) => {event.preventDefault; handleSubmit(uuid, bufferComments, ticker, date )}}
                  variant="contained"
                  color="primary"
                  disabled={bufferComments == comments}
          >
            Save
          </Button>
        </Grid>
      </Grid>
    </div>
  )
}
