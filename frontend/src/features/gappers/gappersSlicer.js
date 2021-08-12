import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import axiosInstance from '../../components/axios'
const axios = require('axios');
const initialState = {
  gappers: [],
  status: 'idle',
  error: null,
  selected: null,
  gapperSelectedStatus: 'idle',
  isFetchingMore: false,
  dates: [],
  oldestDate:''
}

export const fetchGappers = createAsyncThunk('gappers/fetchGappers', async () => (
  axios
  .get(`${process.env.NEXT_PUBLIC_API_URL}/data/`)
    .then(response => response.data)
    .catch(error => {console.log('error fetching gappers', error)})
));

export const fetchGapper = createAsyncThunk('gappers/fetchGapper', async (id) => {
  console.log('id is ', id)
  if(id != undefined){
    return(
      axiosInstance
      .get(`${process.env.NEXT_PUBLIC_API_URL}/gappers/${id}/`)
        .then(response => response.data)
        .catch(error => {console.log('error fetching 1 gapper', error)})
    )
  }
});

export const fetchMoreGappers = createAsyncThunk('gappers/fetchMoreGappers', async (oldest) => {
  console.log('oldest thunk', oldest)
  return (
    axios
    .get(`${process.env.NEXT_PUBLIC_API_URL}/data/`, { params: {oldest: oldest} })
      .then(response => response.data)
      .catch(error => {console.log('error fetching gappers', error)})
  )});

const gapperSlice = createSlice({
  name:'gappers',
  initialState,
  reducers:{
    selectGapper(state, action){
      state.selected = state.gappers.filter((gapper) => gapper.date == action.payload.date && gapper.ticker == action.payload.ticker  )[0]
    },
    setisFetchingMore(state, action){
      state.isFetchingMore = action.payload
    },
    setDates(state, action){
      var dates = [];
      state.gappers.map(gapper => {if(!dates.includes(gapper.date)){dates.push(gapper.date)}})
        var ordererByDayGappers = {}
        dates.forEach((date, i) => {
          var gs = state.gappers.filter(gapper => gapper.date === date)
          ordererByDayGappers[date] = gs
      });
      state.dates = dates;
    },
    setOldesDate(state, action){
      if(state.dates.length > 0 ){
        const oldest = state.dates.reduce((c, n) =>
            Date.parse(n) < Date.parse(c) ? n : c
        );
        state.oldestDate = oldest;
      }
    }
  },
  extraReducers: {
    [fetchGappers.pending]: (state, action) => {
      state.status = 'loading'
    },
    [fetchGappers.fulfilled]: (state, action) => {
      state.status = 'succeeded'
      state.gappers = state.gappers.concat(action.payload)
    },
    [fetchGappers.rejected]: (state, action) => {
      state.status = 'failed'
      state.error = action.error.message
    },
    [fetchGapper.pending]: (state, action) => {
      state.gapperSelectedStatus = 'loading'
    },
    [fetchGapper.fulfilled]: (state, action) => {
      state.gapperSelectedStatus = 'succeeded'
      state.selected = action.payload
    },
    [fetchGapper.rejected]: (state, action) => {
      state.gapperSelectedStatus = 'failed'
      state.selected = null
      state.error = action.error.message
    },
    [fetchMoreGappers.pending]: (state, action) => {
      state.status = 'loadingMore'
    },
    [fetchMoreGappers.fulfilled]: (state, action) => {
      state.status = 'succeeded'
      state.gappers = state.gappers.concat(action.payload)
      state.isFetchingMore = false
    },
    [fetchMoreGappers.rejected]: (state, action) => {
      state.status = 'failed'
      state.error = action.error.message
    },
  }
})

export default gapperSlice.reducer

export const { selectGapper, setisFetchingMore, setDates, setOldesDate } = gapperSlice.actions;

export const selectAllGappers = state => state.gappers.gappers
