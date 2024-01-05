// ================================================================================================
//  File Name: ColumnFrom.js
//  Description: Details of the Discover Data ( Search Data ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { Fragment, useState, useEffect } from 'react'
import {
  Row,
  Col,
  Card,
  Table,
  Spinner,
  Badge
} from 'reactstrap'
import axios from "@axios"
import { token } from '@utils'
import { toast } from 'react-toastify'
import "./tableStyle.css"
import { useTranslation } from 'react-i18next'
import { format } from 'date-fns'

let scrollPosition = 200 //value of div height
let scrollPositionIncrement = 200 //value of div height
const scrollPositionLimit = 20
let scrollPositionOffset = 20
let searchTableScrollData = []
let dNotF = true

const SearchTable = ({ tableData, searchVal }) => {
  const { t } = useTranslation()
  const [loading, setLoading] = useState(false)
  const [searchTableData, setSearchTableData] = useState([])
  searchTableScrollData = tableData

  function handleScroll(event) {
    scrollPosition = event.target.clientHeight
    if (dNotF) {
      if ((event.target.scrollHeight - event.target.scrollTop) === scrollPosition && !loading) {

        scrollPosition = scrollPosition += scrollPositionIncrement
        scrollPositionOffset = scrollPositionOffset += scrollPositionLimit

        setLoading(true)
        axios.get(`/innovative-search-api?search_val=${searchVal.search_val}&col_name=${searchVal.col_name}&limit=${scrollPositionLimit}&offset=${scrollPositionOffset}`, { headers: { Authorization: token() } })
          .then(res => {

            if (res.data.message_type === "data_ok") {
              for (let i = 0; i < res.data.data.length; i++) {
                searchTableScrollData.push(res.data.data[i])
              }
              setSearchTableData(searchTableScrollData)
            }

            if (res.data.message_type === "data_not_found") {
              if (dNotF) {
                toast.warn("Data Not Found.", {
                  position: "top-right",
                  autoClose: 5000,
                  hideProgressBar: false,
                  closeOnClick: true,
                  pauseOnHover: true,
                  draggable: true,
                  progress: undefined
                })
              }
              dNotF = false
            }

            scrollPositionIncrement = event.target.clientHeight
          }).finally(() => {
            setLoading(false)
          })
      }
    }
  }

  useEffect(() => {
    document.querySelector(".searchTableScrollRef > .table-responsive").addEventListener('scroll', handleScroll, { passive: true })
    setSearchTableData(tableData)
    scrollPosition = 200
    scrollPositionIncrement = 200
    scrollPositionOffset = 20
    dNotF = true
  }, [tableData])

  const renderTableData = searchTableData.map((val, key) => {
    return (
      <tr key={key}>
        <td className='text-uppercase'><Badge color='light-secondary'>{format(new Date(val.attack_timestamp), "yyyy-MM-dd, h:mm:ss a")}</Badge></td>
        <td><Badge color='danger'>{val.attacker_ip}</Badge></td>
        <td><Badge color='light-primary'>{val.target_ip}</Badge></td>
        <td><Badge color='danger'>{val.attacker_mac}</Badge></td>
        <td><Badge color='light-warning'>{val.target_mac_address}</Badge></td>
        <td><Badge color='danger'>{val.attack_os}</Badge></td>
        <td><Badge color='light-secondary'>{val.target_os}</Badge></td>
        <td><Badge color='light-danger'>{val.ids_threat_class}</Badge></td>
        <td><Badge color='light-primary'>{val.ml_threat_class}</Badge></td>
        <td><Badge color='light-info'>{val.dl_threat_class}</Badge></td>
        <td><Badge color='light-danger'>{val.ids_threat_type}</Badge></td>
        <td><Badge color='light-danger'>{val.ids_threat_severity}</Badge></td>
        <td><Badge color='light-primary'>{val.ml_accuracy}</Badge></td>
        <td><Badge color='light-info'>{val.dl_accuracy}</Badge></td>
        <td><Badge color='light-secondary'>{val.type_of_threat}</Badge></td>
        <td><Badge color='light-warning'>{val.platform}</Badge></td>
        <td><Badge color='warning'>{val.tcp_port}</Badge></td>
        <td><Badge color='warning'>{val.udp_port}</Badge></td>
        <td><Badge color='warning'>{val.icmp_port}</Badge></td>
        {/* <td>{val['@timestamp']}</td> */}
        <td><Badge color='light-success'>{val.geoip_asn_name}</Badge></td>
        <td><Badge color='light-success'>{val.geoip_country_name}</Badge></td>
        <td><Badge color='light-success'>{val.geoip_latitude}</Badge></td>
        <td><Badge color='light-success'>{val.geoip_longitude}</Badge></td>
        <td><Badge color='light-success'>{val.geoip_city}</Badge></td>
        <td><Badge color='light-success'>{val.geoip_postal_code}</Badge></td>
      </tr>
    )
  })

  return (
    <Fragment>
      <Row className='export-component'>
        <Col sm='12'>
          <Card>
            <div className='searchTableScrollRef p-0'>
              {loading ? <div style={{ backgroundColor: "transparent", position: "absolute", width: "100%", height: "100%", zIndex: 99999, paddingTop: "20rem" }} className="d-flex justify-content-center">
                <Spinner animation="border" type='grow' color='primary' />
              </div> : ""
              }
              <Table className='table-hover-animation mt-2 p-0' responsive>
                <thead>
                  <tr>
                    <th>{t('Attacker Timestamp')}</th>
                    <th>{t('Attacker IPs')}</th>
                    <th>{t('Target IP')}</th>
                    <th>{t('Attacker Mac')}</th>
                    <th>{t('Target Mac')}</th>
                    <th>{t('Attacker OS')}</th>
                    <th>{t('Target OS')}</th>
                    <th>{t('Ids Threat Class')}</th>
                    <th>{t('Ml Threat Class')}</th>
                    <th>{t('Dl Threat Class')}</th>
                    <th>{t('Ids Threat Type')}</th>
                    <th>{t('Ids Threat Severity')}</th>
                    <th>{t('Ml Accuracy')}</th>
                    <th>{t('Dl Accuracy')}</th>
                    <th>{t('Type of Threat')}</th>
                    <th>{t('Platform')}</th>
                    <th>{t('Tcp')}</th>
                    <th>{t('Udp')}</th>
                    <th>{t('Icmp')}</th>
                    {/* <th>Timestamp</th> */}
                    <th>{t('Ans')}</th>
                    <th>{t('Country Name')}</th>
                    <th>{t('Latitude')}</th>
                    <th>{t('Longititude')}</th>
                    <th>{t('City')}</th>
                    <th>{t('Postal')}</th>
                  </tr>
                </thead>
                <tbody>{renderTableData}</tbody>
              </Table>
            </div>
          </Card>
        </Col>
      </Row>
    </Fragment>
  )
}

export default SearchTable
