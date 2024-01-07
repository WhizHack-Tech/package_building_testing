// ** Third Party Components
import { useTranslation } from 'react-i18next'
export let data
export const Ip = () => {
  const { t } = useTranslation()
  return [
    {
      name: t('Attacker IPs'),
      selector: 'attacker_ip',
      sortable: true,
      minWidth: '100px'
    },
    {
      name: t('Attacker Mac Address'),
      selector: 'attacker_mac',
      sortable: true,
      minWidth: '150px'
    },
    {
      name: t('No Of Times Attacked'),
      selector: 'count(attacker_ip)',
      sortable: true,
      minWidth: '150px'
    }
  ]
}

export default Ip
