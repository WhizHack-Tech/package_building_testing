// ================================================================================================
//  File Name: ExternalAttacketails.js
//  Description: Details of the NIDS Events ( Extarnal Attack Count )
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { useState, useEffect, useMemo } from "react"
import { useLocation } from 'react-router-dom'
import { ChevronDown } from 'react-feather'
import DataTable from 'react-data-table-component'
import { Card, CardHeader, CardTitle } from 'reactstrap'
import { token } from '@utils'
import axios from '@axios'
import PreLoader from '../preLoader'
import '@styles/react/libs/tables/react-dataTable-component.scss'
import { useTranslation } from 'react-i18next'

const TopAttackedDetails = () => {
    const {t} = useTranslation()
    const { search } = useLocation()
    const searchParams = useMemo(() => new URLSearchParams(search), [search])
    const [apiLoader, setApiLoader] = useState(false)
    const [tableData, setTableData] = useState([])

    const DetailsApiLogic = () => {
        setApiLoader(true)
        axios.get(`/nids-alert-ext-table?past_time=${searchParams.get('past_time')}&current_time=${searchParams.get('current_time')}&name=${searchParams.get('name')}`, { headers: { Authorization: token() } })
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
    const columnsName = [
        {
            name: t('Timestamp'),
            sortable: true,
            selector: row => row.attack_timestamp,
            minWidth: '180px'
        },
        {
            name: t('Type of Threat'),
            sortable: true,
            selector: row => row.type_of_threat,
            minWidth: '260px'
        },
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
            name: t('Attacker Port'),
            sortable: true,
            selector: row => row.attacker_port,
            minWidth: '80px'
        },
        {
            name: t('IDS Threat Class'),
            sortable: true,
            selector: row => row.ids_threat_class,
            minWidth: '250px'
        },
        {
            name: t('IDS Threat Type'),
            sortable: true,
            selector: row => row.ids_threat_type,
            minWidth: '410px'
        },
        {
            name: t('DL Threat Class'),
            sortable: true,
            selector: row => row.dl_threat_class,
            minWidth: '410px'
        },
        {
            name: t('ML Threat Class'),
            sortable: true,
            selector: row => row.ml_threat_class,
            minWidth: '280px'
        },
        {
            name: t('DL Confident'),
            sortable: true,
            selector: row => row.dl_accuracy,
            minWidth: '100px'
        },
        {
            name: t('ML Confident'),
            sortable: true,
            selector: row => row.ml_accuracy,
            minWidth: '100px'
        },
        {
            name: t('ASN Name'),
            sortable: true,
            selector: row => row.geoip_asn_name,
            minWidth: '100px'
        },
        {
            name: t('Country'),
            sortable: true,
            selector: row => row.geoip_country_name,
            minWidth: '200px'
        }
    ]
    return (
        <Card className='overflow-hidden'>
            <CardHeader>
                <CardTitle>
                    {t('External Attacks')} : {searchParams.get('name')}
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