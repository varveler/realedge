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
					'A server/network error occurred. ' +
						'Looks like CORS might be the problem. ' +
						'Sorry about this - we will get it fixed shortly.'
				);
				return Promise.reject(error);
			}

			if (
				error.response.status === 401 &&
				originalRequest.url === baseURL + 'token/refresh/'
			) {
				window.location.href = '/signin/';
				return Promise.reject(error);
			}

			if (
				error.response.data.code === 'token_not_valid' &&
				error.response.status === 401 &&
				error.response.statusText === 'Unauthorized'
			) {
				const refreshToken = localStorage.getItem('refresh_token_reio');

				if (refreshToken) {
					const tokenParts = JSON.parse(atob(refreshToken.split('.')[1]));

					// exp date in token is expressed in seconds, while now() returns milliseconds:
					const now = Math.ceil(Date.now() / 1000);
					console.log(tokenParts.exp);

					if (tokenParts.exp > now) {
						return axiosInstance
							.post('/token/refresh/', { refresh: refreshToken })
							.then((response) => {
								sessionStorage.setItem('access_token', response.data.access);
								localStorage.setItem('refresh_token_reio', response.data.refresh);

								axiosInstance.defaults.headers['Authorization'] =
									'JWT ' + response.data.access;
								originalRequest.headers['Authorization'] =
									'JWT ' + response.data.access;

								return axiosInstance(originalRequest);
							})
							.catch((err) => {
								console.log(err);
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
