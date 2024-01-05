import { useTranslation } from 'react-i18next'

export let data

// ** Table Zero Config Column
export const Columns = () => {
  const {t} = useTranslation()
  return [
    {
      name: t('Target IP'),
      selector: 'target_ip',
      sortable: true,
      minWidth: '80px'
    },
    {
      name: t('Target Mac Address'),
      selector: 'target_mac_address',
      sortable: true,
      minWidth: '150px'
    },
    {
      name: t('No Of Times Attacked'),
      selector: 'count(target_ip)',
      sortable: true,
      minWidth: '150px'
    }
  ]
}
//** Expandable table component
const ExpandableTable = ({ data }) => {
  const {t} = useTranslation()
  return (
    <div className='expandable-content p-2'>
      <p>
        <span className='font-weight-bold'>City:</span> {data.city}
      </p>
      <p>
        <span className='font-weight-bold'>Experience:</span> {data.experience}
      </p>
      <p className='m-0'>
        <span className='font-weight-bold'>Post:</span> {data.post}
      </p>
    </div>
  )
}

export default ExpandableTable
