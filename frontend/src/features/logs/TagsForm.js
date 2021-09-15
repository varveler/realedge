import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';
import Autocomplete, { createFilterOptions } from '@material-ui/lab/Autocomplete';
import { getTags, postTags, putTags, deleteTags } from './logsSlicer';
import Dialog from '@material-ui/core/Dialog';
import DialogTitle from '@material-ui/core/DialogTitle';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogActions from '@material-ui/core/DialogActions';
import Button from '@material-ui/core/Button';

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
  const asTagsOptions = tags.filter(tag => tag.type_display == 'Assertion')

  const filter = createFilterOptions();
  const [value, setValue] = useState(null);
  const [open, toggleOpen] = useState(false);


  const handleClose = () => {
    setDialogValue({
      name: '',
      type: ''
    });
    toggleOpen(false);
  };

  const [dialogValue, setDialogValue] = useState({
    name: '',
    type: '',
  });

  const handleSubmit = (event, type) => {
    event.preventDefault();
    setValue({
      name: dialogValue.name,
      type: type,
    });
    handleClose();
  };



  useEffect(() => {
    if(ticker != undefined && date != undefined){
      dispatch(getTags({ticker, date}))
    };
  },[])


  // so smelly and spaguetti --> to refactor latter
  const handleChange = (event, newTags, type) =>{
    //console.log(newTags)
    const selectedTags = tags.filter(tag => tag.selected)
    const addedTag = newTags.filter(tag => !selectedTags.includes(tag))
    const removedTag = selectedTags.filter(tag => !newTags.includes(tag) && tag.type == type)
    if(addedTag.length >= 1){
      //console.log('addedTag', addedTag)
      if(tags.includes(addedTag[0])){ //its an already created tag, just dispatch a put
        dispatch(putTags({ticker:ticker, date:date, ...addedTag[0]}))
      }else if (typeof addedTag[0] === 'string') { //the user entered text and hitted enter check if there is an existing tag whit thtat text / name
        var alreadyExistingTag = tags.filter(tag => tag.name === addedTag[0] && tag.type === type)
        if(alreadyExistingTag.length >= 1){
          dispatch(putTags({ticker:ticker, date:date, ...alreadyExistingTag[0]}))
        }else{
          dispatch(postTags({ticker:ticker, date:date, name:addedTag[0], type:type}))
        }
      }else if (addedTag[0].adding){ //the user clicked on option to add new tag
        var alreadyExistingTag = tags.filter(tag => tag.name === addedTag[0].name && tag.type === addedTag[0].type)
        if(alreadyExistingTag.length >= 1){
          dispatch(putTags({ticker:ticker, date:date, ...alreadyExistingTag[0]}))
        }else{
          dispatch(postTags({ticker:ticker, date:date, ...addedTag[0]}))
      }
      }
    }else if (removedTag.length >= 1) {
      //console.log('removedTag', removedTag[0].name)
      dispatch(deleteTags({ticker:ticker, date:date, ...removedTag[0]}))
    }
  }

  const filterAuto = (options, params, type, typeDisplay) => {
    const filtered = filter(options, params);
    if (params.inputValue !== '') {
      filtered.push({
        inputValue: params.inputValue,
        name: params.inputValue,
        type_display : typeDisplay,
        type: type,
        selected: false,
        adding: true
      });
    }
    return filtered;
  }


  const giveOptions = (option) => {
    // e.g value selected with enter, right from the input
    if (typeof option === 'string') {
      return option;
    }
    if (option.inputValue) {
      return 'add new '+ '"'+option.inputValue +'"'+ ' tag';
    }
    return option.name;
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
            value={asTags}
            onChange={(event, newValue) => {handleChange(event, newValue, 'AS') }}
            filterOptions={(options, params) => filterAuto(options, params, 'AS', 'Assertion')}
            multiple
            selectOnFocus
            clearOnBlur
            handleHomeEndKeys
            id={"AStags"}
            options={tags.filter(tag => tag.type_display == 'Assertion')}
            getOptionLabel={(option) => giveOptions(option)}
            freeSolo
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
            value={neTags}
            onChange={(event, newValue) => {handleChange(event, newValue, 'NE') }}
            filterOptions={(options, params) => filterAuto(options, params, 'NE', 'Neutral')}
            multiple
            selectOnFocus
            clearOnBlur
            handleHomeEndKeys
            id={"NEtags"}
            options={tags.filter(tag => tag.type_display == 'Neutral')}
            getOptionLabel={(option) => giveOptions(option)}
            freeSolo
            renderInput={(params) => (
              <TextField
                {...params}
                variant="outlined"
                label={'Neutral'}
              />
            )}
          />
        </Grid>
        <Grid item xs={4}>
          <Autocomplete
            value={erTags}
            onChange={(event, newValue) => {handleChange(event, newValue, 'ER') }}
            filterOptions={(options, params) => filterAuto(options, params, 'ER', 'Error')}
            multiple
            selectOnFocus
            clearOnBlur
            handleHomeEndKeys
            id={"ERtags"}
            options={tags.filter(tag => tag.type_display == 'Error')}
            getOptionLabel={(option) => giveOptions(option)}
            freeSolo
            renderInput={(params) => (
              <TextField
                {...params}
                variant="outlined"
                label={'Error'}
              />
            )}
          />
        </Grid>
      </Grid>
    </div>
  )
}
