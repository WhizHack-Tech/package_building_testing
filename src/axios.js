import axios from "axios"

// const _baseURL = "http://127.0.0.1:8000"
const _baseURL = "https://<<CLIENT-DOMAIN-URL>>"

const instance = axios.create({
    baseURL: `${_baseURL}/api`
})

// URLs Objects
const urlObj = new URL(_baseURL)

// Determine WebSocket protocol dynamically
const WebSocketProtocol = urlObj.protocol === "https:" ? "wss" : "ws"

export const staticPath = _baseURL
export const wsURL = `${WebSocketProtocol}://${urlObj.host}/ws`
export default instance