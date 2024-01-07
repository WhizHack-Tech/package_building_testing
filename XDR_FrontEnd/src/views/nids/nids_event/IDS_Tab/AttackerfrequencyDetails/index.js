// ================================================================================================
//  File Name: index.js
//  Description: Details of the NIDS Events IDS ( Attacker Frequency Details )
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { useState, useEffect } from "react"
import { Card, CardHeader, CardTitle, CardBody } from 'reactstrap'
import { ChevronDown } from 'react-feather'
import DataTable from 'react-data-table-component'
import { useSelector } from 'react-redux'
import axios from '@axios'
import PreLoader from '../../preLoader'
import { useTranslation } from 'react-i18next'
import { token } from '@utils'

const TopAttackedDetails = () => {
  const {t} = useTranslation()
  const [apiLoader, setApiLoader] = useState(false)
  const [tableData, setTableData] = useState([])
  const [dataFound, setDataFound] = useState(true)
  const filterState = useSelector((store) => store.dashboard_chart)
  const [checkApiData, setCheckApiData] = useState(true)
  const DetailsApiLogic = () => {
    setApiLoader(true)
    axios.get(`/nids-event-freq-attacker?condition=${filterState.values ? filterState.values : 'last_1_hour'}`, { headers: { Authorization: token() } })
      .then(res => {
        setApiLoader(false)

        if (res.data.message_type === "d_not_f") {
          setCheckApiData(false)
        }

        if (res.data.message_type === "success") {
          setCheckApiData(true)
          setTableData(res.data.data)
        }

      })
      .catch(error => {
        setApiLoader(false)
        console.log(error.message)
      })
  }

  useEffect(() => {
    DetailsApiLogic()
  }, [filterState.values, filterState.refreshCount])

  const columnsName = [
    {
      name: t('Source IP'),
      sortable: true,
      selector: row => row.attacker_ip,
      minWidth: '120px'
    },
    {
      name: t('Count'),
      sortable: true,
      selector: row => row.attacker_ip_count,
      minWidth: '20px'
    },
    {
      name: t('Destination Mac'),
      sortable: true,
      selector: row => row.target_mac,
      minWidth: '160px'
    }
    // {
    //   name: 'Threat Type',
    //   sortable: true,
    //   selector: row => row.type_of_threat,
    //   minWidth: '260px'
    // }
  ]

  return (
    <Card className='overflow-hidden'>
      <CardHeader>
        <CardTitle>
          {t('Frequent Attacker Details')}
        </CardTitle>
      </CardHeader>
      <CardBody>
        {checkApiData ? (
          <div className='react-dataTable'>
            <DataTable
              noHeader
              pagination
              data={tableData}
              columns={columnsName}
              className='react-dataTable'
              sortIcon={<ChevronDown size={5} />}
              paginationPerPage={5}
              paginationRowsPerPageOptions={[5, 10, 25, 50, 100]}
            />
          </div>
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

export default TopAttackedDetails
