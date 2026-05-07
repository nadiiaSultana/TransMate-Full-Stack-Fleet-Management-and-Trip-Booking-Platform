import {createContext,useContext,useState} from 'react';
import axiosInstance from '../api/axiosInstance';
const AuthContext=createContext();
export const AuthProvider=({children})=>{const stored=localStorage.getItem('user'); const [user,setUser]=useState(stored?JSON.parse(stored):null); const login=async(username,password)=>{const r=await axiosInstance.post('/auth/login/',{username,password}); localStorage.setItem('user',JSON.stringify(r.data.user)); localStorage.setItem('accessToken',r.data.tokens.access); localStorage.setItem('refreshToken',r.data.tokens.refresh); setUser(r.data.user); return r.data.user}; const logout=()=>{localStorage.clear(); setUser(null)}; return <AuthContext.Provider value={{user,login,logout,setUser}}>{children}</AuthContext.Provider>};
export const useAuth=()=>useContext(AuthContext);
