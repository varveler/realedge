import { configureStore } from '@reduxjs/toolkit'

import gappersReducers from './features/gappers/gappersSlicer'

export default configureStore({
  reducer: {
    gappers : gappersReducers
  }
})
