import { redirect } from "react-router-dom"

export function getAuthToken(){
    const token = localStorage.getItem('token')
    if(!token) {
        return null
    }
    return token
}
export function checkToken(){
    const token = getAuthToken()
    if(!token){
        redirect('/login')
    }
}

export function LoadToken(){
    return getAuthToken()
}