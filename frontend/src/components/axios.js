import axios from 'axios';

const baseURL = process.env.NEXT_PUBLIC_API_URL;
const ISSERVER = typeof window === "undefined";
let axiosInstance;


if(!ISSERVER){
	 axiosInstance = axios.create({
		baseURL: baseURL,
		timeout: 5000,
		headers: {
			Authorization: sessionStorage.getItem('access_token')
				? 'JWT ' + sessionStorage.getItem('access_token')
				: null,
			'Content-Type': 'application/json',
			accept: 'application/json',
		  'Access-Control-Allow-Origin': '*'
		},
	});

	axiosInstance.interceptors.response.use(
		(response) => {
			return response;
		},
		async function (error) {
			const originalRequest = error.config;

			if (typeof error.response === 'undefined') {
				alert(
					'Sorry! An error occurred. ' +
						'We will get it fixed ASAP.'
				);
				return Promise.reject(error);
			}
			console.log('error.response', error.response)
			if (
				error.response.status === 401 &&
				originalRequest.url === baseURL + '/token/refresh/'
			) {
				window.location.href = '/signin/';
				return Promise.reject(error);
			}

			if (
				error.response.data.code === 'token_not_valid' &&
				error.response.status === 401 &&
				error.response.statusText === 'Unauthorized'
			) {
				const refreshToken = localStorage.getItem('refresh_token');

				if (refreshToken) {
					const tokenParts = JSON.parse(atob(refreshToken.split('.')[1]));

					// exp date in token is expressed in seconds, while now() returns milliseconds:
					const now = Math.ceil(Date.now() / 1000);

					if (tokenParts.exp > now) {
						return axiosInstance
							.post('/token/refresh/', { refresh: refreshToken })
							.then((response) => {
								sessionStorage.setItem('access_token', response.data.access);
								//localStorage.setItem('refresh_token', response.data.refresh);

								axiosInstance.defaults.headers['Authorization'] =
									'JWT ' + response.data.access;
								originalRequest.headers['Authorization'] =
									'JWT ' + response.data.access;

								return axiosInstance(originalRequest);
							})
							.catch((err) => {
								console.log('er1', err);
							});
					} else {
						console.log('Refresh token is expired', tokenParts.exp, now);
						window.location.href = '/signin/';
					}
				} else {
					console.log('Refresh token not available.');
					window.location.href = '/signin/';
				}
			}

			// specific error handling done elsewhere
			return Promise.reject(error);
		}
	);
}else{
 axiosInstance = axios.create({
  baseURL: baseURL,
  timeout: 5000,
	headers: {
		'Content-Type': 'application/json',
		accept: 'application/json',
	},
});
}


export default axiosInstance;
