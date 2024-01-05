// ** Custom Components
import Avatar from '@components/avatar'

// ** Third Party Components
import axios from 'axios'
import { useTranslation } from 'react-i18next'
// ** Vars
//const states = ['success', 'danger', 'warning', 'info', 'dark', 'primary', 'secondary']

const data_source_id = {
  3: { title: 'Offline', color: 'light-primary' },
  2: { title: 'Active', color: 'light-success' },
  0: { title: 'IDS', color: 'light-warning' },
  1: { title: 'USML', color: 'light-danger' },
  5: { title: 'Vulnerable', color: 'light-info' }
}
const attack_threat_severity = {
  0: { title: 'Milt', color: 'light-primary' },
  1: { title: 'Moderate', color: 'light-info' },
  2: { title: 'Severe', color: 'light-warning' },
  3: { title: 'Critical', color: 'light-danger' },
  4: { title: 'Normal', color: 'light-success' }
}

export let data


export const Fastest = () => {
  const { t } = useTranslation()
  return [
    {
      name: t('Attacker IPs'),
      selector: 'attacker_ip',
      sortable: true,
      minWidth: '150px'
    },
    {
      name: t('Most Attacked Services'),
      selector: 'service_name',
      sortable: true,
      minWidth: '150px'
    },
    {
      name: t('No Of Times Attacked'),
      selector: 'count(service_name)',
      sortable: true,
      minWidth: '150px'
    }
  ]
}


export default Fastest
