import React, { Fragment } from 'react';
import GapperDetail from './../../features/gappers/GapperDetail'
import NavBar from './../../features/navbar/NavBar'

const GapperDetailView = () => {
    return (
        <Fragment>
          <NavBar />
          <GapperDetail />
        </Fragment>
    )
}

export default GapperDetailView
