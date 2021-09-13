import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
import { getTags, postTags, putTags, deleteTags } from './logsSlicer';


const useStyles = makeStyles((theme) => ({
  containerTags:{
    marginTop: '45px',
  },
  tradeComents: {
    marginTop: '25px'
  }
}))

export default function TagsForm({ticker, date, type}){
  const classes = useStyles();
  const dispatch = useDispatch();
  const {tags} = useSelector(state => state.logs)
  const erTags = tags.filter(tag => tag.type_display == 'Error' && tag.selected)
  const asTags = tags.filter(tag => tag.type_display == 'Assertion' && tag.selected)
  const neTags = tags.filter(tag => tag.type_display == 'Neutral' && tag.selected)

  useEffect(() => {
    if(ticker != undefined && date != undefined){
      dispatch(getTags({ticker, date}))
    };
  },[])



  const handleChange = (event, newTags, type) =>{
    console.log(tags)
    const selectedTags = tags.filter(tag => tag.selected)
    const addedTag = newTags.filter(tag => !selectedTags.includes(tag))
    const removedTag = selectedTags.filter(tag => !newTags.includes(tag) && tag.type == type)
    if(addedTag.length >= 1){
      console.log('addedTag', addedTag[0].name)
      dispatch(putTags({ticker:ticker, date:date, ...addedTag[0]}))
    }else if (removedTag.length >= 1) {
      console.log('removedTag', removedTag[0].name)
      dispatch(deleteTags({ticker:ticker, date:date, ...removedTag[0]}))
    }
  }

  return (
    <div className={classes.containerTags}>
      <Grid container
            direction="row"
            justifyContent="space-around"
            alignItems="center"
            spacing={5}>
        <Grid item xs={4}>
          <Autocomplete
            multiple
            onChange={(event, value) => {handleChange(event, value, 'AS')}}
            id={"AStags"}
            options={tags.filter(tag => tag.type_display == 'Assertion')}
            getOptionLabel={(tag) => tag.name}
            value={asTags}
            renderInput={(params) => (
              <TextField
                {...params}
                variant="outlined"
                label={'Assertions'}
              />
            )}
          />
        </Grid>
        <Grid item xs={4}>
        <Autocomplete
          multiple
          id={"NEtags"}
          options={tags.filter(tag => tag.type_display == 'Neutral')}
          getOptionLabel={(tag) => tag.name}
          onChange={(event, value) => {handleChange(event, value, 'NE')}}
          value={neTags}
          renderInput={(params) => (
            <TextField
              {...params}
              variant="outlined"
              label={"Neutral"}
            />
          )}
        />
        </Grid>
        <Grid item xs={4}>
        <Autocomplete
          multiple
          id={"ERtags"}
          options={tags.filter(tag => tag.type_display == 'Error')}
          getOptionLabel={(tag) => tag.name}
          onChange={(event, value) => {handleChange(event, value, 'ER')}}
          value={erTags}
          renderInput={(params) => (
            <TextField
              {...params}
              variant="outlined"
              label={"Errors"}
            />
          )}
        />
        </Grid>
      </Grid>
    </div>
  )
}
