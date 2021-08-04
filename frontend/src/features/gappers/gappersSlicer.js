import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import axiosInstance from '../../components/axios'
const axios = require('axios');
const initialState = {
  gappers: [],
  status: 'idle',
  error: null,
  gapperSelected: null,
  gapperSelectedStatus: 'idle'
}

export const fetchGappers = createAsyncThunk('gappers/fetchGappers', async () => (
  axios
  .get(`${process.env.NEXT_PUBLIC_API_URL}/data/`)
    .then(response => response.data)
    .catch(error => {console.log('error fetching gappers', error)})
));

export const fetchGapper = createAsyncThunk('gappers/fetchGapper', async (id) => {
  if(id != undefined){
    return(
      axiosInstance
      .get(`${process.env.NEXT_PUBLIC_API_URL}/gappers/${id}/`)
        .then(response => response.data)
        .catch(error => {console.log('error fetching 1 gapper', error)})
    )
  }
});


const gapperSlice = createSlice({
  name:'gappers',
  initialState,
  reducers:{
    selectGapper(state, action){
      state.gapperSelected = state.gappers.filter((gapper) => gapper.date == action.payload.date && gapper.ticker == action.payload.ticker  )[0]
    }
  },
  extraReducers: {
    [fetchGappers.pending]: (state, action) => {
      state.status = 'loading'
    },
    [fetchGappers.fulfilled]: (state, action) => {
      state.status = 'succeeded'
      // Add any fetched gappers to the array
      //console.log('action fetch gappers action: ', action)

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
      state.gapperSelected = action.payload
    },
    [fetchGapper.rejected]: (state, action) => {
      state.gapperSelectedStatus = 'failed'
      state.gapperSelected = null
      state.error = action.error.message
    },
  }
})

export default gapperSlice.reducer

export const { selectGapper } = gapperSlice.actions;

export const selectAllGappers = state => state.gappers.gappers
