import { configureStore } from '@reduxjs/toolkit'

import gappersReducers from './features/gappers/gappersSlicer'
import navBarReducers from './features/navbar/navBarSlicer'
import tradesReducers from './features/trades/tradesSlicer'
import accessReducers from './features/access/accessSlicer'
import chartsReducers from './features/charts/chartsSlicer'

export default configureStore({
  reducer: {
    gappers : gappersReducers,
    navbar: navBarReducers,
    trades: tradesReducers,
    access: accessReducers,
    charts: chartsReducers
  },
})
