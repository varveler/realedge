import React, { Fragment } from 'react';
import TradeDetail from './../../features/trades/TradeDetail'
import NavBar from './../../features/navbar/NavBar'

const TradeDetailView = () => {
    return (
        <Fragment>
          <NavBar />
          <TradeDetail />
        </Fragment>
    )
}

export default TradeDetailView
