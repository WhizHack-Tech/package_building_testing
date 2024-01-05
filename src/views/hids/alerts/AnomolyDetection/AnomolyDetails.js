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
        axios.get(`/hids-alert-anomaly-table?past_time=${searchParams.get('past_time')}&current_time=${searchParams.get('current_time')}&agent_id=${searchParams.get('agent_id')}&agent_ip=${searchParams.get('agent_ip')}&anomaly_label_count=${searchParams.get('anomaly_label_count')}`, { headers: { Authorization: token() } })
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
            name: t('Agent ID'),
            sortable: true,
            selector: row => row.agent_id,
            minWidth: '50px'
        },
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
            minWidth: '150px'
        },
        // {
        //     name: t('Agent Location'),
        //     sortable: true,
        //     selector: row => row.agent_location,
        //     minWidth: '150px'
        // },
        {
            name: t('Agent Name'),
            sortable: true,
            selector: row => row.agent_name,
            minWidth: '200px'
        },
        // {
        //     name: t('Decoder Name'),
        //     sortable: true,
        //     selector: row => row.decoder_name,
        //     minWidth: '200px'
        // },
        // {
        //     name: t('Manger Name'),
        //     sortable: true,
        //     selector: row => row.manager_name,
        //     minWidth: '150px'
        // },
        // {
        //     name: t('Rule ID'),
        //     sortable: true,
        //     selector: row => row.rule_id,
        //     minWidth: '50px'
        // },
        {
            name: t('Rule Description'),
            sortable: true,
            selector: row => row.rule_description,
            minWidth: '230px'
        },
        // {
        //     name: t('Rule Firedtimes'),
        //     sortable: true,
        //     selector: row => row.rule_firedtimes,
        //     minWidth: '80px'
        // },
        // {
        //     name: t('Rule GDPR'),
        //     sortable: true,
        //     selector: row => row.rule_gdpr,
        //     minWidth: '100px'
        // },
        // {
        //     name: t('Rule Gpg13'),
        //     sortable: true,
        //     selector: row => row.rule_gpg13,
        //     minWidth: '100px'
        // },
        // {
        //     name: t('Rule Group'),
        //     sortable: true,
        //     selector: row => row.rule_groups,
        //     minWidth: '100px'
        // },
        // {
        //     name: t('Rule Hipaa'),
        //     sortable: true,
        //     selector: row => row.rule_hipaa,
        //     minWidth: '150px'
        // },
        // {
        //     name: t('Rule level'),
        //     sortable: true,
        //     selector: row => row.rule_level,
        //     minWidth: '80px'
        // },
        // {
        //     name: t('Rule Mitre ID'),
        //     sortable: true,
        //     selector: row => row.rule_mitre_id,
        //     minWidth: '100px'
        // },
        {
            name: t('Rule Mitre Tactic'),
            sortable: true,
            selector: row => row.rule_mitre_tactic,
            minWidth: '120px'
        },
        {
            name: t('Rule Mitre technique'),
            sortable: true,
            selector: row => row.rule_mitre_technique,
            minWidth: '200px'
        },
        {
            name: t('Anomaly Label'),
            sortable: true,
            selector: row => row.anomaly_label,
            minWidth: '100px'
        }
        // {
        //     name: t('Rule PCI DSS'),
        //     sortable: true,
        //     selector: row => row.rule_pci_dss,
        //     minWidth: '100px'
        // },
        // {
        //     name: t('Rule TSC'),
        //     sortable: true,
        //     selector: row => row.rule_tsc,
        //     minWidth: '100px'
        // }
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
                <CardTitle tag='h4'> {t("Anomaly Details")} : {searchParams.get("agent_ip")}</CardTitle>
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