// ================================================================================================
//  File Name: sensorDetails.js
//  Description: Details of the Health Check ( Sensor Details ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { useState, useEffect, useMemo } from "react"
import { useLocation } from 'react-router-dom'
import { ChevronDown, Share, FileText, Grid } from 'react-feather'
import DataTable from 'react-data-table-component'
import {
    Card, CardHeader, CardTitle, DropdownMenu,
    DropdownItem,
    DropdownToggle,
    UncontrolledButtonDropdown
} from 'reactstrap'
import { token } from '@utils'
import axios from '@axios'
import PreLoader from '../../preLoader'
import { useTranslation } from 'react-i18next'
import '@styles/react/libs/tables/react-dataTable-component.scss'
import XLSX from "xlsx"
import { CSVLink } from "react-csv"
import { saveAs } from "file-saver"

const SensorDetails = () => {
    const { t } = useTranslation()
    const { search } = useLocation()
    const searchParams = useMemo(() => new URLSearchParams(search), [search])
    const [apiLoader, setApiLoader] = useState(false)
    const [tableData, setTableData] = useState([])

    const DetailsApiLogic = () => {
        setApiLoader(true)
        axios.get(`/hc-level-line-table?past_time=${searchParams.get('past_time')}&current_time=${searchParams.get('current_time')}&sensor_id=${searchParams.get('sensor_id')}&sensor_type=${searchParams.get('sensor_type')}&level=${searchParams.get('level')}`, { headers: { Authorization: token() } })
            .then(res => {
                setApiLoader(false)
                if (res.data.message_type === "success") {
                    setTableData(res.data.table)
                }
            })
            .catch(error => {
                setApiLoader(false)
            })
    }

    useEffect(() => {
        DetailsApiLogic()
    }, [])

    const columnsName = [
        {
            name: t('Timestamp'),
            sortable: true,
            selector: row => row.timestamp,
            wrap: true,
            width: "200px"
        },
        {
            name: t('Log Info'),
            sortable: true,
            selector: row => row.level,
            wrap: true
        },
        {
            name: t("Sensor ID"),
            sortable: true,
            selector: row => row.sensor_id,
            wrap: true
        },
        {
            name: t("IP Address"),
            sortable: true,
            selector: row => row.ip_address,
            wrap: true
        },
        {
            name: t("CPU Utilization"),
            sortable: true,
            selector: row => row.cpu_utilization,
            wrap: true
        },
        {
            name: t("RAM Utilization"),
            sortable: true,
            selector: row => row.ram_utilization,
            wrap: true
        },
        {
            name: t("Disk Remaining"),
            sortable: true,
            selector: row => row.disk_remaining,
            wrap: true
        },
        {
            name: t("Disk Log Details"),
            sortable: true,
            selector: row => row.disk_action,
            wrap: true
        },
        {
            name: t("Sensor Name"),
            sortable: true,
            selector: row => row.sensor_name,
            wrap: true,
            width: "250px"
        }
    ]

    const exportToXLSX = () => {
        const fileType = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=UTF-8"
        const fileExtension = ".xlsx"
        const formattedData = tableData.map((item) => ({
            ...item,
            attack_timestamp: new Date(item.attack_timestamp).toLocaleString() // Format timestamp if needed
        }))
        const ws = XLSX.utils.json_to_sheet(formattedData)
        const wb = { Sheets: { data: ws }, SheetNames: ["data"] }
        const excelBuffer = XLSX.write(wb, { bookType: "xlsx", type: "array" })
        const data = new Blob([excelBuffer], { type: fileType })
        const fileName = `Report_Download${fileExtension}`
        saveAs(data, fileName)
    }

    const exportToCSV = () => {
        const formattedData = tableData.map((item) => ({
            ...item,
            attack_timestamp: new Date(item.attack_timestamp).toLocaleString() // Format timestamp if needed
        }))
        return formattedData
    }

    return (
        <Card className='overflow-hidden'>
            <CardHeader className='flex-md-row flex-column align-md-items-center align-items-start border-bottom'>
                <CardTitle tag='h4'>{t('Sensor Details')}</CardTitle>
                <div className='d-flex mt-md-0 mb-1 mt-1'>
                    <UncontrolledButtonDropdown>
                        <DropdownToggle color='secondary' caret outline>
                            <Share size={15} />
                            &nbsp;
                            <span className='align-middle ms-50'>{t('Export')}</span>
                        </DropdownToggle>
                        <DropdownMenu>
                            &nbsp;   &nbsp;&nbsp;&nbsp;
                            <CSVLink
                                data={exportToCSV()}
                                filename={"Report_Download.csv"}
                            >
                                <FileText size={15} />
                                <span className='align-middle ms-50'>{t('CSV')}</span>
                            </CSVLink>
                            <DropdownItem className='w-100' onClick={exportToXLSX}>
                                <Grid size={15} />
                                <span className='align-middle ms-50'>{t('Excel')}</span>
                            </DropdownItem>
                        </DropdownMenu>
                    </UncontrolledButtonDropdown>
                </div>
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

export default SensorDetails