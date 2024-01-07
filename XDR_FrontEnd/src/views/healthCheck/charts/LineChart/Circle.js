// ================================================================================================
//  File Name: Circle.js
//  Description: Details of the Health Check ( Ram Utilization ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import React from 'react'
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar'
import 'react-circular-progressbar/dist/styles.css'

const RamUtilizationProgressBar = ({ ramUtilization }) => {
    return (
        <div className='d-flex align-items-center'>
            <div style={{ width: "30px" }} className='mr-1'>
                <CircularProgressbar
                    value={ramUtilization}
                    text={`${ramUtilization}%`}
                    styles={buildStyles({
                        textSize: '0px',
                        pathColor: '#FF0000',
                        textColor: '#f88',
                        trailColor: `rgba(62, 152, 199,0.2)`
                    })}
                />
            </div>
            <span>{`${ramUtilization} Mbps`}</span>
        </div>
    )
}

export default RamUtilizationProgressBar