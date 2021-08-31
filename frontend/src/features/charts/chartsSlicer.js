import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import axiosInstance from '../../components/axios'

//const axios = require('axios');
const initialState = {
  data: [], //{oneMin:[], fiveMin:[], day:[]},
  status: 'idle',
  error: null,
  _from:null,
  to:null
}


//https://data.alpaca.markets//v2/stocks/AAPL/bars?start=2021-04-06T09:01:00Z&end=2021-04-10T22:01:00Z&timeframe=1Min
export const fetchBarsTrade = createAsyncThunk('chart/fetchBarsTrade', async (uuids) => {
  const url = `${process.env.NEXT_PUBLIC_API_URL}/charts/trade?${uuids.map((n, index) => `trade[]=${n}`).join('&')}`
  console.log('url',url)
  return (
  axiosInstance
  .get(url)
  .then(response => {
    return response.data
  })
  .catch(error => {console.log('error fetching bars', error)})
)});


export const fetchBarsGapper = createAsyncThunk('chart/fetchBarsGapper', async (data) => {
  const {slug} = data;
  return (
  axiosInstance
  .get(`${process.env.NEXT_PUBLIC_API_URL}/charts/gapper/${slug}/`)
  .then(response => {
    return response.data
  })
  .catch(error => {console.log('error fetching bars', error)})
)});

const chartsSlice = createSlice({
  name:'charts',
  initialState,
  reducers:{
    setFetchChartStatus(state, action){
      state.status = action.payload
      state.data = []
    },
    setFromTo(state, action){
      state._from = action.payload._from
      state.to = action.payload.to
    },
    cleanFromTo(state, action){
      state._from = ''
      state.to = ''
    }
  },
  extraReducers: {
    [fetchBarsTrade.pending]: (state, action) => {
      state.status = 'loading'
    },
    [fetchBarsTrade.fulfilled]: (state, action) => {
      state.status = 'succeeded'
      state.data = action.payload },
    [fetchBarsTrade.rejected]: (state, action) => {
      state.status = 'failed'
      state.error = action.error.message
    },
    [fetchBarsGapper.pending]: (state, action) => {
      state.status = 'loading'
    },
    [fetchBarsGapper.fulfilled]: (state, action) => {
      state.status = 'succeeded'
      state.data = action.payload },
    [fetchBarsGapper.rejected]: (state, action) => {
      state.status = 'failed'
      state.error = action.error.message
    }
  }
})

export default chartsSlice.reducer

export const { setFetchChartStatus, setFromTo, cleanFromTo } = chartsSlice.actions;

//export const selectAllTrades = state => state.trades.trades
