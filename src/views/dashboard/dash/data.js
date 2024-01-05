// Filename : data.js
// Purpose/Description : The data getting from this file to table
// Author : Jaydeep Roy Sarkar (EMP-0020), Danish Ansari (EMP-0037) and Sai Kaladhar (EMP-0017)
// Copyright (c) : Whizhack Technologies (P) Ltd.
import { Badge, Progress } from 'reactstrap'
import { useTranslation } from 'react-i18next'
import { format } from 'date-fns'
const threat_severity = {
  1: { title: 'High', color: 'light-danger' },
  2: { title: 'Medium', color: 'light-warning' },
  3: { title: 'Low', color: 'light-info' }
}
// ** Expandable table component
const ExpandableTable = ({ data }) => {
  const { t } = useTranslation()
  return (
    <div className='expandable-content p-2'>
      <div className='d-flex justify-content-start align-items-center mb-1 mt-1'>
        <span className='font-weight-bold mr-1'>{t('ML Accuracy')}:</span>
        <Progress className='progress-bar-primary w-25' value={data.ml_accuracy}>
          {data.ml_accuracy}%
        </Progress>
        <span className='font-weight-bold ml-3 mr-1'>{t('ML Engine')}:</span> <Badge color='primary'>{data.ml_threat_class}</Badge>
      </div>
      <div className='d-flex justify-content-start align-items-center mb-1 mt-1 m-0'>
        <span className='font-weight-bold mr-1'>{t('DL Accuracy')}:</span>
        <Progress className='progress-bar-info w-25' value={data.dl_accuracy}>
          {data.dl_accuracy}%
        </Progress>
        <span className='font-weight-bold ml-3 mr-1'>{t('DL Engine')}:</span> <Badge color='info'>{data.dl_threat_class}</Badge>
      </div>
    </div>
  )
}

// ** Table Common Column
export const Columns = () => {
  const { t } = useTranslation()
  return [
    {
      name: t('Activity'),
      selector: 'ids_threat_class',
      sortable: true,
      minWidth: '250px',
      cell: row => {
        return (
          <div>
            <Badge color='danger'>{row.ids_threat_class}</Badge>
          </div>
        )
      }
    },
    {
      name: t('Type of Threat'),
      selector: 'type_of_threat',
      sortable: true,
      minWidth: '200px',
      cell: row => {
        return (
          <div>
            <Badge color='info'>{row.type_of_threat}</Badge>
          </div>
        )
      }
    },
    {
      name: t('Platform'),
      selector: 'platform',
      sortable: true,
      minWidth: '150px',
      cell: row => {
        return (
          <div>
            <Badge color='light-danger'>{row.platform}</Badge>
          </div>
        )
      }
    },
    {
      name: t('Threat Severity'),
      selector: 'ids_threat_severity',
      sortable: true,
      minWidth: '150px',
      cell: row => {

        return (
          <Badge color={threat_severity[row.ids_threat_severity].color} pill>
            {threat_severity[row.ids_threat_severity].title}
          </Badge>
        )
      }
    },
    {
      name: t('Attacker IPs'),
      selector: 'attacker_ip',
      sortable: true,
      minWidth: '150px'
    },
    {
      name: t('Attacker MAC'),
      selector: 'attacker_mac',
      sortable: true,
      minWidth: '200px'
    },
    {
      name: t('Attack Timestamp'),
      selector: 'target_timestamp',
      sortable: true,
      minWidth: '200px',
      cell: row => {
        return (
          <div className='d-flex justify-content-left align-items-center'>
            <Badge color='light-primary'>
              <span className='font-weight-bold text-uppercase'>{format(new Date(row.target_timestamp), "yyyy-MM-dd, h:mm:ss a")}</span>
            </Badge>
          </div>
        )
      }

    },
    {
      name: t('Target IP'),
      selector: 'target_ip',
      sortable: true,
      minWidth: '150px'
    },
    {
      name: t('Target MAC'),
      selector: 'target_mac_address',
      sortable: false,
      minWidth: '250px'
    }
  ]
}

export default ExpandableTable