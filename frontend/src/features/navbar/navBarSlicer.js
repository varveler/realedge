import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  activeTab: false
}


const navBarSlice = createSlice({
  name:'navbar',
  initialState,
  reducers:{
    navbarSelected(state, action) {
      state.activeTab = action.payload
    },

  }
});

export const {navbarSelected} = navBarSlice.actions

export default navBarSlice.reducer

export const selectActiveTab = state => state.navbar.activeTab
