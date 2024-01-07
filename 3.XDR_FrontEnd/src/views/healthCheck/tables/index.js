import React, { Fragment, useState, memo } from 'react'
import { ChevronDown, Eye } from 'react-feather'
import DataTable from 'react-data-table-component'
import { Card, CardHeader, CardTitle, CardBody, Input } from 'reactstrap'
import { Link } from 'react-router-dom'
import '@styles/react/libs/tables/react-dataTable-component.scss'
import { useTranslation } from 'react-i18next'

const TablesData = ({ tableTitle, tableData, pastTime, currentTime, filteCondition }) => {
    const { t } = useTranslation()
    const [searchValue, setSearchValue] = useState('')

    const handleSearch = e => {
        setSearchValue(e.target.value.trim())
    }

    const filteredData = tableData.filter(item => {
        const sensorId = String(item.sensor_id)
        const sensorName = String(item.sensor_name)
        const sensortype = String(item.sensor_type)

        return (
            sensorId.toLowerCase().includes(searchValue.toLowerCase()) ||
            sensorName.toLowerCase().includes(searchValue.toLowerCase()) ||
            sensortype.toLowerCase().includes(searchValue.toLowerCase())
        )
    })

    const basicColumns = [
        {
            name: t('Sensor ID'),
            selector: 'sensor_id',
            sortable: true,
            maxWidth: '400px'
        },
        {
            name: t('Sensor Name'),
            selector: 'sensor_name',
            sortable: true
        },
        {
            name: t('Sensor Type'),
            selector: 'sensor_type',
            sortable: true
        },
        {
            name: t('Timestamp'),
            selector: 'attack_epoch_time',
            sortable: true
        },
        {
            name: t('Actions'),
            selector: 'sensor_id',
            cell: rowData => {
                return <Link to={`/health-check/sensor-types?sensor_id=${rowData.sensor_id}&sensor_type=${rowData.sensor_type}&past_time=${pastTime}&current_time=${currentTime}&condition=${filteCondition}`}>
                    <Eye />
                </Link>
            }
        }
    ]

    return (
        <Fragment>
            <Card>
                <CardHeader className="align-items-center justify-content-between m-1">
                    <CardTitle tag='h2'>{tableTitle}</CardTitle>
                    <Input
                        type='text'
                        placeholder={t('Search')}
                        className='form-control w-25'
                        value={searchValue}
                        onChange={handleSearch}
                    />
                </CardHeader>

                <CardBody>
                    {tableData.length > 0 ? (
                        <div className='react-dataTable mb-2'>
                            <DataTable
                                noHeader
                                pagination
                                data={filteredData}
                                columns={basicColumns}
                                className='react-dataTable '
                                sortIcon={<ChevronDown size={5} />}
                                paginationPerPage={7}
                                paginationRowsPerPageOptions={[7, 10, 25, 50, 100]}
                            />
                        </div>
                    ) : (
                        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
                            <p>{t('Data Not Found')}</p>
                        </div>
                    )}
                </CardBody>
            </Card >
        </Fragment>
    )
}

export default memo(TablesData)
