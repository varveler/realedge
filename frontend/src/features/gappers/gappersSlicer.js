import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'

const axios = require('axios');
const initialState = {
  gappers: [],
  status: 'idle',
  error: null
}



export const fetchGappers = createAsyncThunk('gappers/fetchGappers', async () => (
  axios
  .get(`${process.env.NEXT_PUBLIC_API_URL}/data/`)
    .then(response => {console.log('rd', response.data); return response.data})
    .catch(error => {console.log('error fetching gappers', error)})
));

const gapperSlice = createSlice({
  name:'gappers',
  initialState,
  reducers:{

  },
  extraReducers: {
    [fetchGappers.pending]: (state, action) => {
      state.status = 'loading'
    },
    [fetchGappers.fulfilled]: (state, action) => {
      state.status = 'succeeded'
      // Add any fetched gappers to the array
      console.log('action', action)
      state.gappers = state.gappers.concat(action.payload)
    },
    [fetchGappers.rejected]: (state, action) => {
      state.status = 'failed'
      state.error = action.error.message
    },
  }
})

export default gapperSlice.reducer

export const selectAllGappers = state => state.gappers.gappers
