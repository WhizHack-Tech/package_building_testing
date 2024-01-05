// ================================================================================================
//  File Name: IPSDetails.js
//  Description: Details of the NIDS Alerts ( Attacker Target ip's).
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
import PreLoader from '../preLoader'
import { useTranslation } from 'react-i18next'
import XLSX from "xlsx"
import { CSVLink } from "react-csv"
import { saveAs } from "file-saver"


const AttackerIpsDetails = () => {
    const { search } = useLocation()
    const searchParams = useMemo(() => new URLSearchParams(search), [search])
    const {t} = useTranslation()
    const [apiLoader, setApiLoader] = useState(false)
    const [tableData, setTableData] = useState([])

    const DetailsApiLogic = () => {
        setApiLoader(true)
        axios.get(`/nids-alert-attacker-ip-line-table?past_time=${searchParams.get('past_time')}&current_time=${searchParams.get('current_time')}&attacker_ip=${searchParams.get('attacker_ip')}&platform=${searchParams.get('platform')}`, { headers: { Authorization: token() } })
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
            name: t('Platform'),
            sortable: true,
            selector: row => row.platform,
            wrap: true,
            width: "100px"
        },
        {
            name: t('Type of Threat'),
            sortable: true,
            selector: row => row.type_of_threat,
            wrap: true,
            width: "200px"
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
            wrap: true,
            width: "100px"
        },
        {
            name: t('IDS Threat Class'),
            sortable: true,
            selector: row => row.ids_threat_class,
            wrap: true,
            width: "250px"
        },
        {
            name: t('IDS Threat Type'),
            sortable: true,
            selector: row => row.ids_threat_type,
            wrap: true,
            width: "400px"
        },
        {
            name: t('DL Threat Class'),
            sortable: true,
            selector: row => row.dl_threat_class,
            wrap: true,
            width: "250px"
        },
        {
            name: t('ML Threat Class'),
            sortable: true,
            selector: row => row.ml_threat_class,
            wrap: true,
            width: "200px"
        },
        {
            name: t('DL Confident'),
            sortable: true,
            selector: row => row.dl_accuracy,
            wrap: true,
            width: "150px"
        },
        {
            name: t('ML Confident'),
            sortable: true,
            selector: row => row.ml_accuracy,
            wrap: true,
            width: "150px"
        },
        {
            name: t('ASN Name'),
            sortable: true,
            selector: row => row.geoip_asn_name,
            wrap: true,
            width: "150px"
        },
        {
            name: t('Country'),
            sortable: true,
            selector: row => row.geoip_country_name,
            wrap: true,
            width: "150px"
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
                <CardTitle tag='h4'>{t('Source IPs')} : {searchParams.get('attacker_ip')}</CardTitle>
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
                    responsive={true}
                />
            </div>

            {apiLoader ? <PreLoader /> : null}
        </Card>
    )
}

export default AttackerIpsDetails