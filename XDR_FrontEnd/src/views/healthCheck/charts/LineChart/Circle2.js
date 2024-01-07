// ================================================================================================
//  File Name: Circle2.js
//  Description: Details of the Health Check ( Download Speed ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import React from 'react'
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar'
import 'react-circular-progressbar/dist/styles.css'

const RamUtilizationProgressBar = ({ download_speed }) => {
    return (
        <div className='d-flex align-items-center'>
            <div style={{ width: "30px" }} className='mr-1'>
                <CircularProgressbar
                    value={download_speed}
                    text={`${download_speed}%`}
                    styles={buildStyles({
                        textSize: '0px',
                        pathColor: '#ff9f43',
                        textColor: '#f88',
                        trailColor: `rgba(62, 152, 199,0.2)`
                    })}
                />
            </div>
            <span>{`${download_speed} Mbps`}</span>
        </div>
    )
}

export default RamUtilizationProgressBar