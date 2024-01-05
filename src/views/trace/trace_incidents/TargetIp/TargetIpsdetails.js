// ================================================================================================
//  File Name: TargetIpsdetails.js
//  Description: Details of the Trace ( Incidents ( target IP's Details )).
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
import { useTranslation } from 'react-i18next'
import PreLoader from '../../preLoader'
import XLSX from "xlsx"
import { CSVLink } from "react-csv"
import { saveAs } from "file-saver"

const TargetIPDetails = () => {
    const {t} = useTranslation()
    const { search } = useLocation()
    const searchParams = useMemo(() => new URLSearchParams(search), [search])

    const [apiLoader, setApiLoader] = useState(false)
    const [tableData, setTableData] = useState([])

    const DetailsApiLogic = () => {
        setApiLoader(true)
        axios.get(`/incident-trget-ip-table-trace?past_time=${searchParams.get('past_time')}&current_time=${searchParams.get('current_time')}&name=${searchParams.get('name')}&name1=${searchParams.get('name1')}`, { headers: { Authorization: token() } })
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
            name: t('Sensor Name'),
            sortable: true,
            selector: row => row.sensor_name,
            wrap: true,
            width: "200px"
        },
        {
            name: t('Type of Threat'),
            sortable: true,
            selector: row => row.type_of_threat,
            wrap: true,
            width: "250px"
        },
        {
            name: t('IDS Threat Class'),
            sortable: true,
            selector: row => row.ids_threat_class,
            wrap: true,
            width: "250px"
        },
        // {
        //     name: t('Source MAC'),
        //     sortable: true,
        //     selector: row => row.attacker_mac,
        //     wrap: true,
        //     width: "200px"
        // },
        {
            name: t('IDS Threat Type'),
            sortable: true,
            selector: row => row.ids_threat_type,
            wrap: true,
            width: "400px"
        },
        {
            name: t('Tag'),
            sortable: true,
            selector: row => row.tag,
            wrap: true,
            width: "200px"
        },
        {
            name: t('Source IP'),
            sortable: true,
            selector: row => row.attacker_ip,
            wrap: true,
            width: "200px"
        },
        {
            name: t('Attacker Host Type'),
            sortable: true,
            selector: row => row.attacker_host_type,
            wrap: true,
            width: "200px"
        },
        {
            name: t('Attacker Port'),
            sortable: true,
            selector: row => row.attacker_port,
            wrap: true,
            width: "200px"
        },
        {
            name: t('Attacker OS'),
            sortable: false,
            selector: row => row.attacker_os,
            wrap: true,
            width: "200px"
        },
        {
            name: t('IP rep'),
            sortable: true,
            selector: row => row.ip_rep,
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
            name: t('Target Port'),
            sortable: true,
            selector: row => row.target_port,
            wrap: true,
            width: "200px"
        },
        {
            name: t('Service Name'),
            sortable: true,
            selector: row => row.service_name,
            wrap: true,
            width: "200px"
        },
        {
            name: t('Http URL'),
            sortable: true,
            selector: row => row.http_url,
            wrap: true,
            width: "200px"
        },
        {
            name: t('Brut Username'),
            sortable: true,
            selector: row => row.brut_username,
            wrap: true,
            width: "200px"
        },
        {
            name: t('Brut Password'),
            sortable: true,
            selector: row => row.brut_password,
            wrap: true,
            width: "200px"
        },
        {
            name: t('Intel Spurce Feed Name'),
            sortable: true,
            selector: row => row.intel_source_feed_name,
            wrap: true,
            width: "200px"
        },
        {
            name: t('Country'),
            sortable: true,
            selector: row => row.geoip_country_name,
            wrap: true,
            width: "200px"
        },
        {
            name: t('City'),
            sortable: true,
            selector: row => row.geoip_city,
            wrap: true,
            width: "200px"
        },
        {
            name: t('ASN Name'),
            sortable: true,
            selector: row => row.geoip_asn_name,
            wrap: true,
            width: "200px"
        },
        {
            name: t('Latitude'),
            sortable: true,
            selector: row => row.geoip_latitude,
            wrap: true,
            width: "200px"
        },
        {
            name: t('Longitude'),
            sortable: true,
            selector: row => row.geoip_longitude,
            wrap: true,
            width: "200px"
        },
        {
            name: t('Mitre Tactics ID'),
            sortable: true,
            selector: row => row.mitre_tactics_id,
            wrap: true,
            width: "200px"
        },
        {
            name: t('Mitre Tactics Name'),
            sortable: true,
            selector: row => row.mitre_tactics_name,
            wrap: true,
            width: "200px"
        },
        {
            name: t('Mitre techniques ID'),
            sortable: true,
            selector: row => row.mitre_techniques_id,
            wrap: true,
            width: "200px"
        },
        {
            name: t('Mitre Techniques Name'),
            sortable: true,
            selector: row => row.mitre_techniques_name,
            wrap: true,
            width: "200px"
        },
        {
            name: t('Malware CVE ID'),
            sortable: true,
            selector: row => row.malware_cve_id,
            wrap: true,
            width: "200px"
        },
        {
            name: t('Malware Type'),
            sortable: true,
            selector: row => row.malware_type,
            wrap: true,
            width: "200px"
        },
        // {
        //     name: t('Attack Epoch Time'),
        //     sortable: true,
        //     selector: row => row.attack_epoch_time,
        //     wrap: true,
        //     width: "200px"
        // },
        {
            name: t('Files Name'),
            sortable: true,
            selector: row => row.files_filename,
            wrap: true,
            width: "200px"
        },
        {
            name: t('Files MD5'),
            sortable: true,
            selector: row => row.files_md5,
            wrap: true,
            width: "200px"
        },
        {
            name: t('Files State'),
            sortable: true,
            selector: row => row.files_state,
            wrap: true,
            width: "200px"
        },
        {
            name: t('Anomaly Event'),
            sortable: true,
            selector: row => row.anomaly_event,
            wrap: true,
            width: "200px"
        },
        {
            name: t('Anomaly APP Proto'),
            sortable: true,
            selector: row => row.anomaly_app_proto,
            wrap: true,
            width: "200px"
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
                <CardTitle tag='h4'> {t("Target IP")} : {searchParams.get("name")}</CardTitle>
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

export default TargetIPDetails