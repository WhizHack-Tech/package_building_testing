// ================================================================================================
//  File Name: dNotf.js
//  Description: Details of the NIDS Alerts ( Do Not Found )
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import '@styles/react/libs/tables/react-dataTable-component.scss'
import { useTranslation } from 'react-i18next'
const styles = {
    height: '300px',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center'
}

const DataNotFound = ({ msg }) => {
    const {t} = useTranslation()
    return <div className='text-center' style={styles}> {(msg === undefined) ? <p>{t('Data Not Found')}</p> : msg}</div>
}

export default DataNotFound