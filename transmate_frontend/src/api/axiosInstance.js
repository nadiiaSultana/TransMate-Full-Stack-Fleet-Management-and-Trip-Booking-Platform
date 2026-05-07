import axios from 'axios';
const axiosInstance=axios.create({baseURL:'http://127.0.0.1:8000/api'});
axiosInstance.interceptors.request.use((config)=>{const t=localStorage.getItem('accessToken'); if(t) config.headers.Authorization=`Bearer ${t}`; return config;});
export default axiosInstance;
