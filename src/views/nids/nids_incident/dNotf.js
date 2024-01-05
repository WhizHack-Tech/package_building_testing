// ================================================================================================
//  File Name: dNotf.js
//  Description: Details of the NIDS Incidents ( Data Not Found )
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import '@styles/react/libs/tables/react-dataTable-component.scss'
import { useTranslation } from 'react-i18next'
const styles = {
    height: '350px',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center'
}

const DataNotFound = ({ msg }) => {
    const {t} = useTranslation()
    return <div className='text-center' style={styles}> {(msg === undefined) ? t("Data Not Found") : msg}</div>
}

export default DataNotFound