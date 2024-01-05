// =============================================================================================
//  File Name: option.js
//  Description: Details of the dropdown lists repeater.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { Fragment } from "react"
const Options = ({ options }) => {

    const arr = Array.from({ length : options }, (_, index) => index + 1)

    return (
        <Fragment>
            {arr.map((value) => (
                <option key={value} value={value}>{value}</option>
            ))}
        </Fragment>
    )
}

export default Options