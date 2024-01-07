// ================================================================================================
//  File Name:  MitrapicDetails.js
//  Description: Details of the MitraPIC Table.
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

const TopAttackedCount = () => {
    const {t} = useTranslation()
    const { search } = useLocation()
    const searchParams = useMemo(() => new URLSearchParams(search), [search])
    const [apiLoader, setApiLoader] = useState(false)
    const [tableData, setTableData] = useState([])

    const DetailsApiLogic = () => {
        setApiLoader(true)
        axios.get(`/hids-alert-ransomware-table?past_time=${searchParams.get('past_time')}&current_time=${searchParams.get('current_time')}&agent_id=${searchParams.get('agent_id')}&agent_ip=${searchParams.get('agent_ip')}&ransomware_count=${searchParams.get('ransomware_count')}`, { headers: { Authorization: token() } })
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
            selector: row => row.timestamp,
            minWidth: '180px'
        },
        {
            name: t('Agent IP'),
            sortable: true,
            selector: row => row.agent_ip,
            minWidth: '100px'
        },
        {
            name: t('Agent Name'),
            sortable: true,
            selector: row => row.agent_name,
            minWidth: '100px'
        },
        {
            name: t('Rule Description'),
            sortable: true,
            selector: row => row.rule_description,
            minWidth: '300px'
        },
        {
            name: t('Rule Mitre Tactic'),
            sortable: true,
            selector: row => row.rule_mitre_tactic,
            minWidth: '100px'
        },
        {
            name: t('Rule Mitre technique'),
            sortable: true,
            selector: row => row.rule_mitre_technique,
            minWidth: '100px'
        },
        {
            name: t('Syscheck Path'),
            sortable: true,
            selector: row => row.syscheck_path,
            minWidth: '1200px'
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
                <CardTitle tag='h4'> {t("Ransomware Potential")} : {searchParams.get("agent_ip")}</CardTitle>
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

export default TopAttackedCount