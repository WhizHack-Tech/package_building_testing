
// ================================================================================================
//  File Name: NoInternet.js
//  Description: Details ofno Intrenet Connect".
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { useState, useEffect } from "react"
const NoInternetWork = () => {
    return (
        <div style={{ position: "fixed", top: 2, zIndex: 9999, left:"40%", right:"40%" }}>
            <h6 className='d-inline-block text-warning ml-50 mb-0 shadow p-1 rounded bg-white text-center'>No Internet Connection.Please try again later.</h6>
        </div>
    )
}

const NoInternetConnection = () => {
    
    const [isOnline, setOnline] = useState(true)

    // On initization set the isOnline state.
    useEffect(() => {
        setOnline(navigator.onLine)
    }, [])

    // event listeners to update the state 
    window.addEventListener('online', () => {
        setOnline(true)
    })

    window.addEventListener('offline', () => {
        setOnline(false)
    })

    if (isOnline === false) {
        return <NoInternetWork />
    }
    return <></>
}

export default NoInternetConnection