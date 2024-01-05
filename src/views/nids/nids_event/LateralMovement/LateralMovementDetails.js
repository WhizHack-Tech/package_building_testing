// ================================================================================================
//  File Name: LateralMovementDetails.js
//  Description: Details of the NIDS Events ( LaterAL Movemant  Attack Counts )
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { useState, useEffect, useMemo } from "react"
import { useLocation } from 'react-router-dom'
import { ChevronDown } from 'react-feather'
import DataTable from 'react-data-table-component'
import { token } from '@utils'
import { Card, CardHeader, CardTitle } from 'reactstrap'

import axios from '@axios'
import PreLoader from '../preLoader'
import '@styles/react/libs/tables/react-dataTable-component.scss'
const columnsName = [
    {
        name: t('Source IP'),
        sortable: true,
        selector: row => row.attacker_ip,
        wrap: true,
        width: "150px"
    },
    {
        name: t('Source MAC'),
        sortable: true,
        selector: row => row.attacker_mac,
        wrap: true,
        width: "200px"
    },
    {
        name: t('Destination IP'),
        sortable: true,
        selector: row => row.target_ip,
        wrap: true,
        width: "200px"
    },
    {
        name: 'Attacker Port',
        sortable: true,
        selector: row => row.attacker_port
    },
    {
        name: 'DL Confident',
        sortable: true,
        selector: row => row.dl_accuracy
    },
    {
        name: 'DL Threat Class',
        sortable: true,
        selector: row => row.dl_threat_class
    },
    {
        name: 'Geo IP ASN Name',
        sortable: true,
        selector: row => row.geoip_asn_name
    },
    {
        name: 'Geo IP Country Name',
        sortable: true,
        selector: row => row.geoip_country_name
    },
    {
        name: 'IDS Threat Class',
        sortable: true,
        selector: row => row.ids_threat_class
    },
    {
        name: 'IDS Threat Type',
        sortable: true,
        selector: row => row.ids_threat_type
    },
    {
        name: 'ML Confident',
        sortable: true,
        selector: row => row.ml_accuracy
    },
    {
        name: 'ML Threat Class',
        sortable: true,
        selector: row => row.ml_threat_class
    },
    {
        name: 'Target Port',
        sortable: true,
        selector: row => row.target_port
    },
    {
        name: 'Type of Threat',
        sortable: true,
        selector: row => row.type_of_threat
    },
    {
        name: ' Attack Date Time',
        sortable: true,
        selector: row => row.attack_timestamp
    }
]
const TopAttackedDetails = () => {

    const { search } = useLocation()
    const searchParams = useMemo(() => new URLSearchParams(search), [search])
    const [apiLoader, setApiLoader] = useState(false)
    const [tableData, setTableData] = useState([])

    const DetailsApiLogic = () => {
        setApiLoader(true)
        axios.get(`/nids-alert-lateral-mov-table?past_time=${searchParams.get('past_time')}&current_time=${searchParams.get('current_time')}&name=${searchParams.get('name')}`, { headers: { Authorization: token() } })
            .then(res => {
                setApiLoader(false)
                if (res.data.message_type === "success") {
                    setTableData(res.data.table)
                }
            })
            .catch(error => {
                setApiLoader(false)
                console.log(error.message)
            })
    }

    useEffect(() => {
        DetailsApiLogic()
    }, [])

    return (
        <Card className='overflow-hidden'>
            <CardHeader>
                <CardTitle>
                    Lateral Movement : {searchParams.get('name')}
                </CardTitle>
            </CardHeader>
            <div className='react-dataTable'>
                <DataTable
                    noHeader
                    pagination
                    data={tableData}
                    columns={columnsName}
                    className='react-dataTable'
                    sortIcon={<ChevronDown size={10} />}
                    paginationRowsPerPageOptions={[10, 25, 50, 100]}
                />
            </div>

            {apiLoader ? <PreLoader /> : null}
        </Card>
    )
}

export default TopAttackedDetails