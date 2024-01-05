// ================================================================================================
//  File Name: ws_con.js
//  Description: Details of the WS Con page.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { wsURL } from "@axios"
import { getUserData, isUserLoggedIn } from '@utils'
import { store } from "./redux/storeConfig/store"

let interval = null
let ws = null
let emailId = null
let uId = null
// let random_id = Math.floor(Math.random() * 1000000000000)
const setTimeToReload = 60000

export function wsReCon() {
    if (isUserLoggedIn() !== null) {
        let userObj = getUserData()
        emailId = userObj.email
        uId = userObj.id
        // ws = new WebSocket(`${wsURL}/notification/${random_id}`)
        ws = new WebSocket(`${wsURL}/notification/${uId}`)
    }
}

export function WsCheck() {
    if (ws !== null) {
        console.log("wscheck call ...")
        ws.onmessage = function (e) {

            try {
                const { type, message } = JSON.parse(e.data)
                if (type === "chat" && message.notificationRes?.length > 0) {
                    localStorage.setItem('notification_data', JSON.stringify(message.notificationRes))
                    store.dispatch({ type: 'WS_DATA', payload: message })
                }
            } catch (error) {
                console.error('Error parsing JSON in WP:', error)
            }

        }

        ws.onclose = function (e) {
            console.log('Socket is closed.', e.reason)
            clearInterval(interval)
        }

        ws.onerror = function (err) {
            console.error('Socket encountered error: ', err.message, 'Closing socket')
            ws.close()
            clearInterval(interval)
        }

        ws.onopen = function () {

            ws.send(JSON.stringify({
                message: "",
                email: emailId
            }))

            interval = setInterval(() => {
                console.log('setInterval ws')
                ws.send(JSON.stringify({
                    message: "",
                    email: emailId
                }))
            }, setTimeToReload)
        }
    }
}

export function wsCon() {
    if (ws === null) {
        return { readyState: null }
    }
    return ws
}

export function wsDis() {

    if (ws !== null) {
        ws.close()
        console.log("ws disconnected")
    }

    clearInterval(interval)
}

const { readyState } = wsCon()
if ((readyState === 2) || (readyState === 3) || (readyState === 0) || (readyState === null)) {
    wsDis()
    wsReCon()
    WsCheck()
    console.log("ws connected")
}

setInterval(() => {
    const { readyState } = wsCon()

    if ((readyState === 2) || (readyState === 3) || (readyState === 0) || (readyState === null)) {
        wsDis()
        wsReCon()
        WsCheck()
        console.log("ws connected")
    }

    console.log("ws readyState", readyState)

}, 30000)