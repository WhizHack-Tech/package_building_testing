// ================================================================================================
//  File Name: ThreattypeDetails.js
//  Description: Details of the Trace ( Golbal Threat Feed ( Threat Type Details ) ).
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
import XLSX from "xlsx"
import { CSVLink } from "react-csv"
import { saveAs } from "file-saver"

const CityTable = () => {
    const {t} = useTranslation()
    const { search } = useLocation()
    const searchParams = useMemo(() => new URLSearchParams(search), [search])

    const [apiLoader, setApiLoader] = useState(false)
    const [tableData, setTableData] = useState([])

    const DetailsApiLogic = () => {
        setApiLoader(true)
        axios.get(`/glog-trace-threat-type-table?past_time=${searchParams.get('past_time')}&current_time=${searchParams.get('current_time')}&name=${searchParams.get('name')}&name1=${searchParams.get('name1')}`, { headers: { Authorization: token() } })
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
            wrap: true,
            width: "200px"
        },
        {
            name: t('Malware Details'),
            sortable: true,
            selector: row => row.malware_detail,
            wrap: true,
            width: "150px"
        },
        {
            name: t('Threat Nature'),
            sortable: true,
            selector: row => row.threat_nature,
            wrap: true,
            width: "100px"
        },
        {
            name: t('Threat Severity'),
            sortable: true,
            selector: row => row.threat_severity,
            wrap: true,
            width: "100px"
        },
        {
            name: t('Threat Type'),
            sortable: true,
            selector: row => row.threat_type,
            wrap: true,
            width: "200px"
        },
        {
            name: t('Associated Domain'),
            sortable: true,
            selector: row => row.associated_domain,
            wrap: true,
            width: "200px"
        },
        {
            name: t('Current Status'),
            sortable: true,
            selector: row => row.current_status,
            wrap: true,
            width: "200px"
        },
        {
            name: t('Intel Sourced'),
            sortable: false,
            selector: row => row.intel_source,
            wrap: true,
            width: "200px"
        },
        {
            name: t('Data Source'),
            sortable: true,
            selector: row => row.threat_signature,
            wrap: true,
            width: "300px"
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
                <CardTitle tag='h4'> {t("Threat Type")} : {searchParams.get("name")}</CardTitle>
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
                            {/* <DropdownItem className='w-100' onClick={exportToPDF}>
                                <File size={15} />
                                <span className='align-middle ms-50'>{t('PDF')}</span>
                            </DropdownItem> */}
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

export default CityTable