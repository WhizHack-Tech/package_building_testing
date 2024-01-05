// ================================================================================================
//  File Name:  Mitrattcks.js
//  Description: Details of the Mitreattacks  Graph.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import Chart from 'react-apexcharts'
import { useState, useEffect, useMemo } from 'react'
import { Card, CardHeader, CardTitle, CardBody, Table, Button, Modal, ModalHeader, ModalBody } from 'reactstrap'
import axios from "@axios"
import { Link, useLocation } from 'react-router-dom'
import { useSelector } from "react-redux"
import { useTranslation } from 'react-i18next'
import { token } from '@utils'
import PreLoader from '../../preLoader'

const ApexColumnCharts = ({ direction }) => {
    const {t} = useTranslation()
    const { search } = useLocation()
    const [shortTableData, setTableData] = useState([])
    const [criticalThreatsTotal, setCriticalThreatsTotal] = useState([])
    const searchParams = useMemo(() => new URLSearchParams(search), [search])
    const [apiLoader, setApiLoader] = useState(false)
    const [modalBox, setModalBox] = useState(false)
    // const filterState = useSelector((store) => store.dashboard_chart)
    const [checkApiData, setCheckApiData] = useState(true)
  
    const apiLogic = () => {
        setApiLoader(true)
        axios.get(`/hids-incident-mitre-attack-tactic?agent_id=${searchParams.get('agent_id')}&condition=${searchParams.get('condition')}`, { headers: { Authorization: token() } })
          .then(res => {
            setApiLoader(false)
    
            if (res.data.message_type === "d_not_f") {
              setCheckApiData(false)
            }
    
            if (res.data.message_type === "data_found") {
              setCheckApiData(true)
              setCriticalThreatsTotal(res.data.data)
              setTableData(res.data.filter)
            }
    
          })
          .catch(error => {
            setApiLoader(false)
            console.log(error.message)
          })
      }
    
      useEffect(() => {
        apiLogic()
    
      }, [])
    const options = {
        chart: {
            height: 400,
            type: 'bar',
            stacked: true,
            parentHeightOffset: 0,
            toolbar: {
                show: true
            }
        },
        plotOptions: {
            bar: {
                columnWidth: '15%',
                colors: {
                    backgroundBarColors: [],
                    backgroundBarRadius: 5
                }
            }
        },
        dataLabels: {
            enabled: false
        },
        legend: {
            position: 'top',
            horizontalAlign: 'start'
        },
        colors: ['#826bf8', '#21409F', '#01a14b', '#3EB489', '#F70D1A', '#2916F5', '#F0E68C', '#EDDA74', '#FFD801', '#F4A460', '#C2B280', '#C04000', '#FF6347'],
        stroke: {
            show: true,
            colors: ['transparent']
        },
        grid: {
            xaxis: {
                lines: {
                    show: true
                }
            }
        },
        xaxis: {
            categories: criticalThreatsTotal.labels || []
        },
        fill: {
            opacity: 1
        },
        yaxis: {
            opposite: direction === 'rtl'
        }
    }
    const series = criticalThreatsTotal.series?.length > 0 ? criticalThreatsTotal.series : []
    return (
        <Card>
            <CardHeader className='d-flex flex-md-row flex-column justify-content-md-between justify-content-start align-items-md-center align-items-start'>
                <CardTitle tag='h4'>{t('Mitre Att&ck Tactics')}</CardTitle>
                <div className='round overflow-hidden round overflow-hidden'>
          <Button.Ripple color='flat-primary' size='sm' onClick={() => setModalBox(!modalBox)}>
            {t('View More')}
          </Button.Ripple>
        </div>
        <Modal isOpen={modalBox} toggle={() => setModalBox(!modalBox)} size='xl'>
          <ModalHeader>{t('Mitre Att&ck Tactics')}</ModalHeader>
          <ModalBody>
            <Table striped responsive>
              <thead>
                <tr>
                  <th>{t('Agent ID')}</th>
                  <th>{t('Agent IP')}</th>
                  <th>{t('Rule Mitre Tactic')}</th>
                  <th>{t('Count')}</th>
                  <th>{t('Actions')}</th>
                </tr>
              </thead>
              <tbody>
                {(shortTableData.length === 0 || checkApiData === false) ? (
                <tr>
                  <td colSpan={7} className='text-center'>{t('Data Not Found')}</td>
                </tr>
              ) : (
                  shortTableData.map((rows, index) => {
                    return (
                      <tr key={index}>
                        <td>
                          <span className='align-middle fw-bold'>{rows.agent_id}</span>
                        </td>
                        <td>
                          <span className='align-middle fw-bold'>{rows.agent_ip}</span>
                        </td>
                        <td>
                          <span className='align-middle fw-bold'>{rows.rule_mitre_tactic}</span>
                        </td>
                        <td>
                          <span className='align-middle fw-bold'>{rows.rule_mitre_tactic_count}</span>
                        </td>
                        <td>
                          <Link to={`/hids-incident-security_events_mitre_attack_tactics?current_time=${rows.current_time}&past_time=${rows.past_time}&agent_id=${rows.agent_id}&rule_mitre_tactic=${rows.rule_mitre_tactic}&agent_ip=${rows.agent_ip}`} className='btn-sm btn-outline-primary m-2'>
                            {t('More Details')}
                          </Link>
                        </td>
                      </tr>
                    )
                  })
              )
                }
              </tbody>
            </Table>
          </ModalBody>
        </Modal>
            </CardHeader>
            <CardBody>
        {checkApiData ? (
         <Chart options={options} series={series} type='bar' height={350} />
        ) : (
          <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
            <p>{t('Data Not Found')}</p>
          </div>
        )}
      </CardBody>
      {apiLoader ? <PreLoader /> : null}
        </Card>
    )
}

export default ApexColumnCharts
