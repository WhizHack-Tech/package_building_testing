import { useState, useEffect, useMemo } from "react"
import { useLocation } from 'react-router-dom'
import { ChevronDown } from 'react-feather'
import DataTable from 'react-data-table-component'
import { Card, CardHeader, CardTitle } from 'reactstrap'

import axios from '@axios'
import PreLoader from '../preLoader'

const columnsName = [
    {
        name: 'IDS Threat Class',
        sortable: true,
        selector: row => row.ids_threat_class
    },
    {
        name: 'Target IP',
        sortable: true,
        selector: row => row.target_ip
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

const TopAttackedDetails = () => {

    const { search } = useLocation()
    const searchParams = useMemo(() => new URLSearchParams(search), [search])
    const [apiLoader, setApiLoader] = useState(false)
    const [tableData, setTableData] = useState([])

    const DetailsApiLogic = () => {
        setApiLoader(true)
        axios.get(`nids-dashboard-critical-threats-table?past_time=${searchParams.get('past_time')}&current_time=${searchParams.get('current_time')}&name=${searchParams.get('name')}`)
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
                    Critical Threat Name : {searchParams.get('name')}
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