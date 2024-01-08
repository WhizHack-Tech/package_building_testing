// ================================================================================================
//  File Name: axios.js
//  Description: Details of the Axios ( Basic URl ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// =============================================================================================
import axios from "axios"
const instance = axios.create({
 baseURL: "https://<<MASTER-DOMAIN-URL>>/api"
//  baseURL: "http://127.0.0.1:8002/api"
})

export default instance

export const baseURL = "https://<<MASTER-DOMAIN-URL>>/api"
export const staticPath = "https://<<MASTER-DOMAIN-URL>>/api"
// export const staticPath = "http://127.0.0.1:8002"


// WebSocket URL
export const wsURL = "wss://<<MASTER-DOMAIN-URL>>/ws"
// export const wsURL = "ws://127.0.0.1:8002/ws"
//here work...