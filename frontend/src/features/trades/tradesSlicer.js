import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import axiosInstance from '../../components/axios'

//const axios = require('axios');
const initialState = {
  trades: [],
  status: 'idle',
  error: null,
  tradeSelected: null,
  tradeSelectedStatus: 'idle'
}
export const fetchTrades = createAsyncThunk('trades/fetchTrades', async () => (
  axiosInstance
  .get(`${process.env.NEXT_PUBLIC_API_URL}/trades/trades/`)
    .then(response => (response.data))
    .catch(error => {console.log('error fetching trades', error)})
));
export const submitComment = createAsyncThunk('trades/submitComment', async (data) => {
  return(
  axiosInstance
    .post(`/trades/comment/${data.uuid}/`, {
      comment: data.comment
    })
    .then(response => (response.data))
    .catch(error => {console.log('error post comment', error)})
)});


export const fetchTrade = createAsyncThunk('trades/fetchTrade', async (slug) => {
  if(slug != undefined){
    return(
      axiosInstance
      .get(`${process.env.NEXT_PUBLIC_API_URL}/trades/detail/${slug}/`)
        .then(response => (response.data))
        .catch(error => {console.log('error fetching 1 trade', error)})
    )
  }
});


const tradesSlice = createSlice({
  name:'trades',
  initialState,
  reducers:{
    selectTrade(state, action){
      state.tradeSelected = state.trades.filter((trade) => trade.uuid === action.payload )[0]
    },
    changeComment(state, action) {
      state.tradeSelected.comments = action.payload
    },
  },
  extraReducers: {
    [fetchTrades.pending]: (state, action) => {
      state.status = 'loading'
    },
    [fetchTrades.fulfilled]: (state, action) => {
      state.status = 'succeeded'
      state.trades = state.trades.concat(action.payload)
    },
    [fetchTrades.rejected]: (state, action) => {
      state.status = 'failed'
      state.error = action.error.message
    },
    [fetchTrade.pending]: (state, action) => {
      state.tradeSelectedStatus = 'loading'
    },
    [fetchTrade.fulfilled]: (state, action) => {
      state.tradeSelectedStatus = 'succeeded'
      state.tradeSelected = action.payload
    },
    [fetchTrade.rejected]: (state, action) => {
      state.tradeSelectedStatus = 'failed'
      state.tradeSelected = {}
      state.error = action.error.message
    },
  }
})

export default tradesSlice.reducer

export const { selectTrade, changeComment } = tradesSlice.actions;

export const selectAllTrades = state => state.trades.trades
