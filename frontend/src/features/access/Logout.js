import React, { useState, useEffect } from 'react';
import axiosInstance from '../../components/axios';
import { useDispatch, useSelector } from 'react-redux';
import { logOut, selectUserIsLogedIn} from './accessSlicer'

export default function Logout() {
	const userIsLogedIn = useSelector(selectUserIsLogedIn)
	const dispatch = useDispatch()
	useEffect(() => {
			let token = {refresh_token: localStorage.getItem('refresh_token_reio')}
      dispatch(logOut(token))
      }, [userIsLogedIn, dispatch])



	return <div>Logout</div>;
}
