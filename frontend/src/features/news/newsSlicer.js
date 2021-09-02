import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import axiosInstance from '../../components/axios'

const initialState = {
  news: [],
  newsStatus: 'idle',
  error: null,
  selected:''
}


export const fetchNews = createAsyncThunk('news/fetchNews', async (data) => {
  const {ticker, from, to, userIsLogedIn} = data;
  let endpoint;
  if(userIsLogedIn){
    endpoint = `${process.env.NEXT_PUBLIC_API_URL}/news/${ticker}?from=${from}&to=${to}`
  }else{
    endpoint = `${process.env.NEXT_PUBLIC_API_URL}/news/partialnews/${ticker}?from=${from}&to=${to}`
  }
  return(
    axiosInstance
    .get(endpoint)
      .then(response => response.data)
      .catch(error => {console.log('error fetching news', error)})
)})


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
      state.news = action.payload
    },
    [fetchNews.rejected]: (state, action) => {
      state.newsStatus = 'failed'
      state.error = action.error.message
    },
  }
})


export default newsSlicer.reducer

// export const { } = newsSlicer.actions;
