import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import axiosInstance from '../../components/axios'

//const axios = require('axios');
const initialState = {
  trades: [],
  status: 'idle',
  error: null
}



export const fetchTrades = createAsyncThunk('trades/fetchTrades', async () => (
  axiosInstance
  .get(`${process.env.NEXT_PUBLIC_API_URL}/trades/trades/`)
    .then(response => {console.log('response data trades: ', response.data); return response.data})
    .catch(error => {console.log('error fetching trades', error)})
));

const tradesSlice = createSlice({
  name:'trades',
  initialState,
  reducers:{
  },
  extraReducers: {
    [fetchTrades.pending]: (state, action) => {
      state.status = 'loading'
    },
    [fetchTrades.fulfilled]: (state, action) => {
      state.status = 'succeeded'
      // Add any fetched gappers to the array
      console.log('action', action)
      state.trades = state.trades.concat(action.payload)
    },
    [fetchTrades.rejected]: (state, action) => {
      state.status = 'failed'
      state.error = action.error.message
    },
  }
})

export default tradesSlice.reducer

export const selectAllTrades = state => state.trades.trades
