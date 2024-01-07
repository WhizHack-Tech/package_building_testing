// ================================================================================================
//  File Name: index.js
//  Description: Details of the NIDS Incidents ( Attacked Host Details )
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==========================================================================================
import { useState, useEffect } from "react"
import { ChevronDown } from 'react-feather'
import DataTable from 'react-data-table-component'
import { Card, CardHeader, CardTitle, CardBody } from 'reactstrap'
import { useSelector } from 'react-redux'
import axios from '@axios'
import PreLoader from '../preLoader'
import { token } from '@utils'
import { useTranslation } from 'react-i18next'
const TopAttackedDetails = () => {
    const {t} = useTranslation()
    const [apiLoader, setApiLoader] = useState(false)
    const [tableData, setTableData] = useState([])
    const filterState = useSelector((store) => store.incident_charts)
    const [checkApiData, setCheckApiData] = useState(true)

    const DetailsApiLogic = () => {
        setApiLoader(true)
        axios.get(`/nids-incident-freq-targetted-host?condition=${filterState.values ? filterState.values : 'last_1_hour'}`, { headers: { Authorization: token() } })
            .then(res => {
                setApiLoader(false)

                if (res.data.message_type === "d_not_f") {
                    setCheckApiData(false)
                }

                if (res.data.message_type === "success") {
                    setCheckApiData(true)
                    setTableData(res.data.data)
                }

            })
            .catch(error => {
                setApiLoader(false)
                console.log(error.message)
            })
    }

    useEffect(() => {
        DetailsApiLogic()
    }, [filterState.values, filterState.refreshCount])

    const columnsName = [
        {
            name: t('Count'),
            sortable: true,
            selector: row => row.target_ip_count,
            minWidth: '20px'
        },
        {
            name: t('Destination IP'),
            sortable: true,
            selector: row => row.target_ip,
            minWidth: '120px'
        },
        {
            name: t('Destination Mac'),
            sortable: true,
            selector: row => row.target_mac,
            minWidth: '160px'
        },
        {
            name: t('Threat Type'),
            sortable: true,
            selector: row => row.type_of_threat,
            minWidth: '260px'
        }
    ]

    return (
        <Card className='overflow-hidden'>
            <CardHeader>
                <CardTitle>
                   {t('Attack Count Details')}
                </CardTitle>
            </CardHeader>

            <CardBody>
                {checkApiData ? (
                    <div className='react-dataTable'>
                        <DataTable
                            noHeader
                            pagination
                            data={tableData}
                            columns={columnsName}
                            className='react-dataTable'
                            sortIcon={<ChevronDown size={5} />}
                            paginationPerPage={5}
                            paginationRowsPerPageOptions={[5, 10, 25, 50, 100]}
                        />
                    </div>
                ) : (
                    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
                        <p>{t('Data Not Found')}</p>
                    </div>
                )}
            </CardBody>

            {apiLoader ? <PreLoader /> : null}
        </Card>
    )
}

export default TopAttackedDetails