import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import axiosInstance from '../../components/axios'

const axios = require('axios');
const initialState = {
  userIsLogedIn: false,
  status: 'idle',
  logOutStatus : 'idle',
  error: null
}



export const sendCredentials = createAsyncThunk('access/sendCredentials', async (formData) => {
  let credentials = { email: formData.email, password: formData.password };
  console.log('credentials', credentials)
  return (
  axiosInstance
    .post(`${process.env.NEXT_PUBLIC_API_URL}/token/`,{
          email: formData.email, password: formData.password
    })
    .then(response => {
      console.log('response data access: ', response.data);
      localStorage.setItem('access_token', response.data.access);
			localStorage.setItem('refresh_token', response.data.refresh);
			axiosInstance.defaults.headers['Authorization'] =
				'JWT ' + localStorage.getItem('access_token');
      return response.data
    })
    .catch(error => {console.log('error accessing ', error)})
)});


export const logOut = createAsyncThunk('access/logOut', async (token) => (
  axiosInstance
    .post(`${process.env.NEXT_PUBLIC_API_URL}/user/logout/blacklist/`, token)
    .then(response => {
      console.log('logout response: ', response.data);
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      axiosInstance.defaults.headers['Authorization'] = null;
      return response.data
    })
    .catch(error => {console.log('error accessing ', error)})
));


const accessSlice = createSlice({
  name:'access',
  initialState,
  reducers:{
  },
  extraReducers: {
    [sendCredentials.pending]: (state, action) => {
      state.status = 'loading'
    },
    [sendCredentials.fulfilled]: (state, action) => {
      state.status = 'succeeded'
      console.log('action', action)
      state.userIsLogedIn = true
    },
    [sendCredentials.rejected]: (state, action) => {
      state.status = 'failed'
      state.error = action.error.message
    },
    [logOut.pending]: (state, action) => {
      state.logOutStatus = 'loading'
    },
    [logOut.fulfilled]: (state, action) => {
      state.logOutStatus = 'succeeded'
      state.userIsLogedIn = false
    },
    [logOut.rejected]: (state, action) => {
      state.logOutStatus = 'failed'
      state.error = action.error.message
    },
  }
})

export default accessSlice.reducer

export const selectUserIsLogedIn = state => state.access.userIsLogedIn
