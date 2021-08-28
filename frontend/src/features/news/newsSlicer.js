import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import axiosInstance from '../../components/axios'

const initialState = {
  news: [],
  newsStatus: 'idle',
  error: null
}


export const fetchNews = createAsyncThunk('news/fetchNews', async (ticker) => (
  axiosInstance
  .get(`${process.env.NEXT_PUBLIC_API_URL}/news/${ticker}`)
    .then(response => response.data)
    .catch(error => {console.log('error fetching news', error)})
))


const newsSlicer = createSlice({
  name : 'news',
  initialState,
  reducers: {},
  extraReducers:{
    [fetchNews.pending]: (state, action) => {
      state.newsStatus = 'loading'
    },
    [fetchNews.fulfilled]: (state, action) => {
      state.newsStatus = 'succeeded'
      state.gappers = state.news.concat(action.payload)
    },
    [fetchNews.rejected]: (state, action) => {
      state.newsStatus = 'failed'
      state.error = action.error.message
    },
  }
})


export default newsSlicer.reducer

// export const { } = newsSlicer.actions;
