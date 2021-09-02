import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import axiosInstance from '../../components/axios'

const initialState = {
  comments: null,
  bufferComments: null,
  uuid: null,
  getCommentsStatus: 'idle',
  submitCommentsStatus: 'idle',
  deleteCommentsStatus: 'idle',
  error: null,
}


export const getLogs = createAsyncThunk('logs/getLogs', async (data) => {
  const {ticker, date} = data;
  var endpoint = `${process.env.NEXT_PUBLIC_API_URL}/logs/${ticker}/${date}/`;
  return(
    axiosInstance
    .get(endpoint)
      .then(response => response.data)
      .catch(error => {console.log('error get logs', error)})
)})


export const submitLogs = createAsyncThunk('logs/submitLogs', async (data) => { //POST and PUT
  const {ticker, date, comments, uuid} = data;
  var endpoint = `${process.env.NEXT_PUBLIC_API_URL}/logs/${ticker}/${date}/`
  if(uuid){
    return(
      axiosInstance
      .put(endpoint, {comments:comments, uuid:uuid})
        .then(response => response.data)
        .catch(error => {console.log('error put logs', error)})
    )
  }else{
    return(
      axiosInstance
      .post(endpoint, {comments:comments})
        .then(response => response.data)
        .catch(error => {console.log('error post logs', error)})
  )}
})


export const deleteLogs = createAsyncThunk('logs/deleteLogs', async (data) => {
  const {ticker, date, comments, uuid} = data;
  console.log(data)
  var endpoint = `${process.env.NEXT_PUBLIC_API_URL}/logs/${ticker}/${date}/`;
  return(
    axiosInstance
    .delete(endpoint,  { data: { uuid:uuid }})
      .then(response => response.data)
      .catch(error => {console.log('error delete logs', error)})
)})

const logsSlicer = createSlice({
  name : 'logs',
  initialState,
  reducers: {
    changeComments(state, action) {
      state.bufferComments = action.payload
    }
  },
  extraReducers:{
    [getLogs.pending]: (state, action) => {
      state.getCommentsStatus = 'loading'
    },
    [getLogs.fulfilled]: (state, action) => {
      state.getCommentsStatus = 'succeeded'
      state.comments = action.payload.comments
      state.uuid = action.payload.uuid
    },
    [getLogs.rejected]: (state, action) => {
      state.getCommentsStatus = 'failed'
      state.error = action.error.message
    },
    [submitLogs.pending]: (state, action) => {
      state.submitCommentsStatus = 'loading'
    },
    [submitLogs.fulfilled]: (state, action) => {
      state.submitCommentsStatus = 'succeeded'
      state.comments = action.payload.comments
      state.uuid = action.payload.uuid
    },
    [submitLogs.rejected]: (state, action) => {
      state.submitCommentsStatus = 'failed'
      state.error = action.error.message
    },
    [deleteLogs.pending]: (state, action) => {
      state.deleteCommentsStatus = 'loading'
    },
    [deleteLogs.fulfilled]: (state, action) => {
      state.deleteCommentsStatus = 'succeeded'
      state.comments = null
      state.uuid = null
    },
    [deleteLogs.rejected]: (state, action) => {
      state.deleteCommentsStatus = 'failed'
      state.error = action.error.message
    },
  }
})


export default logsSlicer.reducer

export const { changeComments } = logsSlicer.actions;
