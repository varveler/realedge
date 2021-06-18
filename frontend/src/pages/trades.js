import React, { Fragment } from 'react';
import TradesList from './../features/trades/TradesList'
import NavBar from './../features/navbar/NavBar'

const Home = () => {
    return (
        <Fragment>
          <NavBar />
          <TradesList />
        </Fragment>
    )
}

export default Home
