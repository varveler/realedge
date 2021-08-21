import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import axiosInstance from '../../components/axios'

//const axios = require('axios');
const initialState = {
  trades: [],
  orders: [],
  details:[],
  groupedDetails:[],
  detailGroupedTrades:[],
  tradesGroupedByTicker: [],
  error: null,
  status: 'idle',
  groupedFetchStatus: 'idle',
  fetchTradeDetailsStatus:'idle',
  fetchOrdersStatus: 'idle',
  fetchGroupedTradesDetailsStatus: 'idle',
}


export const fetchOrders = createAsyncThunk('trades/fetchOrders', async (uuids) =>{
  const url = `${process.env.NEXT_PUBLIC_API_URL}/trades/orders?${uuids.map((n, index) => `trade[]=${n}`).join('&')}`
  return(
    axiosInstance
    .get(url)
    .then(response => {console.log(response.data); return(response.data) })
    .catch(error => {console.log('error fetching orders details', error)})
  )}
)

export const fetchTradeDetails = createAsyncThunk('trades/fetchTradeDetails', async (slug) =>{
  if(slug != undefined){

  return(
    axiosInstance
    .get(`${process.env.NEXT_PUBLIC_API_URL}/trades/detail/${slug}`)
    .then(response => {console.log(response.data); return(response.data) })
    .catch(error => {console.log('error fetching trades details', error)})
  )}}
)

export const fetchGroupedTradesDetails = createAsyncThunk('trades/fetchGroupedTradesDetails', async (slug) =>{
  if(slug != undefined){

  return(
    axiosInstance
    .get(`${process.env.NEXT_PUBLIC_API_URL}/trades/groupeddetails/${slug}`)
    .then(response => {console.log(response.data); return(response.data) })
    .catch(error => {console.log('error fetching trades details', error)})
  )}}
)

export const fetchTrades = createAsyncThunk('trades/fetchTrades', async () => (
  axiosInstance
  .get(`${process.env.NEXT_PUBLIC_API_URL}/trades/trades/`)
    .then(response => (response.data))
    .catch(error => {console.log('error fetching trades', error)})
));

export const fetchTradesGroupedByTicker = createAsyncThunk('trades/fetchTradesGroupedByTicker', async () => (
  axiosInstance
  .get(`${process.env.NEXT_PUBLIC_API_URL}/trades/byticker/`)
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


const tradesSlice = createSlice({
  name:'trades',
  initialState,
  reducers:{
    changeComment(state, action) {
      state.tradeSelected.comments = action.payload
    },
    cleanFetchTradeDetailsStatus(state, action){
      state.fetchTradeDetailsStatus = action.payload
      state.details = []
    },
    cleanFetchOrdersStatus(state, action){
      state.fetchOrdersStatus = action.payload
      state.orders = []
    },
    cleanGroupedTradesDetailsFetchStatus(state, action){
      state.fetchGroupedTradesDetailsStatus = action.payload
      state.groupedDetails = []
      state.detailGroupedTrades = []
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
    [fetchTradesGroupedByTicker.pending]: (state, action) => {
      state.groupedFetchStatus = 'loading'
    },
    [fetchTradesGroupedByTicker.fulfilled]: (state, action) => {
      state.groupedFetchStatus = 'succeeded'
      state.tradesGroupedByTicker = state.tradesGroupedByTicker.concat(action.payload)
    },
    [fetchTradesGroupedByTicker.rejected]: (state, action) => {
      state.groupedFetchStatus = 'failed'
      state.tradesGroupedByTicker = []
      state.error = action.error.message
    },
    [fetchTradeDetails.pending]: (state, action) => {
      state.fetchTradeDetailsStatus = 'loading'
    },
    [fetchTradeDetails.fulfilled]: (state, action) => {
      state.fetchTradeDetailsStatus = 'succeeded'
      state.details = state.details.concat(action.payload)
    },
    [fetchTradeDetails.rejected]: (state, action) => {
      state.fetchTradeDetailsStatus = 'failed'
      state.error = action.error.message
    },
    [fetchOrders.pending]: (state, action) => {
      state.fetchOrdersStatus = 'loading'
    },
    [fetchOrders.fulfilled]: (state, action) => {
      state.fetchOrdersStatus = 'succeeded'
      state.orders = state.orders.concat(action.payload)
    },
    [fetchOrders.rejected]: (state, action) => {
      state.fetchOrdersStatus = 'failed'
      state.error = action.error.message
    },
    [fetchGroupedTradesDetails.pending]: (state, action) => {
      state.fetchGroupedTradesDetailsStatus = 'loading'
    },
    [fetchGroupedTradesDetails.fulfilled]: (state, action) => {
      state.fetchGroupedTradesDetailsStatus = 'succeeded';
      state.groupedDetails = action.payload.groupedDetails
      state.detailGroupedTrades = action.payload.detailGroupedTrades
    },
    [fetchGroupedTradesDetails.rejected]: (state, action) => {
      state.fetchGroupedTradesDetailsStatus = 'failed'
      state.error = action.error.message
    },
  }
})

export default tradesSlice.reducer

export const { cleanFetchTradeDetailsStatus, changeComment, cleanFetchOrdersStatus, cleanGroupedTradesDetailsFetchStatus } = tradesSlice.actions;

export const selectAllTrades = state => state.trades.trades
