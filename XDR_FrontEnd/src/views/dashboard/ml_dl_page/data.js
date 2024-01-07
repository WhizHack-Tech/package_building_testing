import { Badge, Progress } from 'reactstrap'
import { useTranslation } from 'react-i18next'
import { format } from 'date-fns'

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
      name: t('Platform'),
      selector: 'platform',
      sortable: true,
      minWidth: '150px',
      cell: row => {
        return (
          <div>
            <Badge color='warning'>{row.platform}</Badge>
          </div>
        )
      }
    },
    {
      name: t('Attack Timestamp'),
      selector: '@timestamp',
      sortable: true,
      minWidth: '200px',
      cell: row => {
        return (
          <div className='d-flex justify-content-left align-items-center'>
            <Badge color='light-primary'>
              <span className='font-weight-bold text-uppercase'>{format(new Date(row['@timestamp']), "yyyy-MM-dd, h:mm:ss a")}</span>
            </Badge>
          </div>
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
      minWidth: '150px'
    },
    {
      name: t('Attacker OS'),
      selector: 'attack_os',
      sortable: true,
      minWidth: '150px'
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
    },
    {
      name: t('Target OS'),
      selector: 'target_os',
      sortable: false,
      minWidth: '250px'
    }
  ]
}

export default ExpandableTable