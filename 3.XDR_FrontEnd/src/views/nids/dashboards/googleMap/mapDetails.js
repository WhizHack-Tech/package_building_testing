import { useState, useEffect, useMemo } from "react"
import { useLocation } from 'react-router-dom'
import { ChevronDown } from 'react-feather'
import DataTable from 'react-data-table-component'
import { Card, CardHeader, CardTitle } from 'reactstrap'

import axios from '@axios'
import PreLoader from '../preLoader'

const columnsName = [
    {
        name: 'Country Name',
        sortable: true,
        selector: row => row.geoip_country_name
    },
    {
        name: 'Region Name',
        sortable: true,
        selector: row => row.geoip_region_name
    },
    {
        name: 'Attacker IPs',
        sortable: true,
        selector: row => row.attacker_ip
    },
    {
        name: 'Attacker Mac Address',
        sortable: true,
        selector: row => row.attacker_mac
    },
    {
        name: 'Target Mac Address',
        sortable: true,
        selector: row => row.target_mac_address
    },
    {
        name: ' Attack Date Time',
        sortable: true,
        selector: row => row.attack_timestamp
    }
]

const MapDetails = () => {
    const { search } = useLocation()
    const searchParams = useMemo(() => new URLSearchParams(search), [search])

    const [apiLoader, setApiLoader] = useState(false)
    const [tableData, setTableData] = useState([])

    const DetailsApiLogic = () => {
        setApiLoader(true)
        axios.get(`/nids-attck-event-geo-table?past_time=${searchParams.get('past_time')}&current_time=${searchParams.get('current_time')}&name=${searchParams.get('name')}`)
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
                    Top Attacked : {searchParams.get('name')}
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

export default MapDetails