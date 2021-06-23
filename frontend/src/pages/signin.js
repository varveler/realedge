import React, { Fragment } from 'react';
import SignIn from './../features/access/SignIn'
import NavBar from './../features/navbar/NavBar'

const LogIn = () => {
    console.log(1)
    return (
        <Fragment>
          <NavBar />
          <SignIn />
        </Fragment>
    )
}

export default LogIn
