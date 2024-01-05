// ================================================================================================
//  File Name: dNotf.js
//  Description: Details of the HIDS (Do Not Found Page).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import '@styles/react/libs/tables/react-dataTable-component.scss'
const styles = {
    height: '350px',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center'
}

const DataNotFound = ({ msg }) => {
    return <div className='text-center' style={styles}> {(msg === undefined) ? "Data Not Found" : msg}</div>
}

export default DataNotFound