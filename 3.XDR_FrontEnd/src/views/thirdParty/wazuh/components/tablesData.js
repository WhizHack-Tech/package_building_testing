import React, { useEffect, useState } from 'react'
import { ChevronDown, Eye } from 'react-feather'
import DataTable from 'react-data-table-component'
import { Card, CardHeader, CardTitle, Spinner, Badge } from 'reactstrap'
import { Link } from 'react-router-dom'
import axios from '@axios'
import '@styles/react/libs/tables/react-dataTable-component.scss'
import { useTranslation } from 'react-i18next'

const TablesData = () => {
    const { t } = useTranslation()
    const [tableData, setTableData] = useState([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        axios.get('/show-unique-agentid').then(response => {
            if (response.data.message_type === "data_found") {
                setTableData(response.data.data)
                setLoading(false)
            }
        })

    }, [])

    const basicColumns = [
        {
            name: t('ID'),
            selector: 'agent_id',
            sortable: true,
            maxWidth: '400px',
            cell: row => {
                return (
                  <div>
                    <Badge color='danger'>{row.agent_id}</Badge>
                  </div>
                )
              }
        },
        {
            name: t('Name'),
            selector: 'agent_name',
            sortable: true,
            minWidth: '450px',
            cell: row => {
                return (
                  <div>
                    <Badge color='warning'>{row.agent_name}</Badge>
                  </div>
                )
              }
        },
        {
            name: t('IP'),
            selector: 'agent_ip',
            sortable: true,
            minWidth: '450px',
            cell: row => {
                return (
                  <div>
                    <Badge color='info'>{row.agent_ip}</Badge>
                  </div>
                )
              }
        },
        {
            name: t('Actions'),
            selector: 'action',
            sortable: true,
            minWidth: '100px',
            cell: rowData => {
                return <><Link to={`/third-party/wazuh/${rowData["agent_id"]}`}><Eye /></Link></>
            }
        }
    ]

    return (
        <Card>
            <CardHeader>
                <CardTitle tag='h4'>{t('Agents')}</CardTitle>
            </CardHeader>
            {loading ? <div style={{ backgroundColor: "transparent", position: "absolute", width: "100%", height: "100%", zIndex: 99999, paddingTop: "20rem" }} className="d-flex justify-content-center"><Spinner animation="border" type='grow' color='primary' /></div> : ""}
            <DataTable
                noHeader
                pagination
                data={tableData}
                columns={basicColumns}
                className='react-dataTable'
                sortIcon={<ChevronDown size={10} />}
                paginationRowsPerPageOptions={[10, 25, 50, 100]}
            />
        </Card>
    )
}

export default TablesData
