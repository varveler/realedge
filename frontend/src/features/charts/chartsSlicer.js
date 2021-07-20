import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import axiosInstance from '../../components/axios'

//const axios = require('axios');
const initialState = {
  data: [], //{oneMin:[], fiveMin:[], day:[]},
  status: 'idle',
  error: null,
  '1Min': [],
  '5Min': [],
  'day':[]
}


//https://data.alpaca.markets//v2/stocks/AAPL/bars?start=2021-04-06T09:01:00Z&end=2021-04-10T22:01:00Z&timeframe=1Min
export const fetchBars = createAsyncThunk('chart/fetchBars', async (data) => {
  const {uuid, timeframe} = data;
  return (
  axiosInstance
  .get(`${process.env.NEXT_PUBLIC_API_URL}/charts/data/${uuid}/`)
  .then(response => {
    // const bars = response.data.map(
    //   function(el){
    //   const newob = {...el, date: new Date(el.date)}; return newob
    //   }
    // )
    // console.log('response data bars bars: ', bars);
    return response.data
  })
  .catch(error => {console.log('error fetching bars', error)})
)});

const chartsSlice = createSlice({
  name:'bars',
  initialState,
  reducers:{
  },
  extraReducers: {
    [fetchBars.pending]: (state, action) => {
      state.status = 'loading'
    },
    [fetchBars.fulfilled]: (state, action) => {
      state.status = 'succeeded'
      state.data = action.payload },
    [fetchBars.rejected]: (state, action) => {
      state.status = 'failed'
      state.error = action.error.message
    }
  }
})

export default chartsSlice.reducer

//export const { reduceFunc } = chartsSlice.actions;

//export const selectAllTrades = state => state.trades.trades
