import React, { Fragment } from 'react';
import GroupedTradesDetail from './../features/trades/GroupedTradesDetail'
import NavBar from './../features/navbar/NavBar'

const TradeDetailView = () => {
    return (
        <Fragment>
          <NavBar />
          <GroupedTradesDetail />
        </Fragment>
    )
}

export default TradeDetailView
