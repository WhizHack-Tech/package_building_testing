// =============================================================================================
//  File Name: cryptoHelper.js
//  Description: Details of the cryptoHelper Utility component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import CryptoJS from 'crypto-js'
const SECRET_KEY_CRYPTO = "abc123fda4213dfr"
const SECRET_KEY = CryptoJS.enc.Utf8.parse(SECRET_KEY_CRYPTO)

export const encryptPlayload = (playload) => {
    if (typeof playload === "string") {
        return CryptoJS.AES.encrypt(playload, SECRET_KEY, { mode: CryptoJS.mode.ECB }).toString()
    } else if (typeof playload === "object") {
        return CryptoJS.AES.encrypt(JSON.stringify(playload), SECRET_KEY, { mode: CryptoJS.mode.ECB }).toString()
    }
}


export const decryptPlayload = (playload, typeOf = "string") => {
    if (typeof playload === "string") {
        let decryptData = CryptoJS.AES.decrypt(playload, SECRET_KEY, { mode: CryptoJS.mode.ECB }).toString(CryptoJS.enc.Utf8)

        if (typeOf === "json") {
            return JSON.parse(decryptData)
        } else {
            return decryptData
        }
    }
}