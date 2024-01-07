   // ================================================================================================
//  File Name: index.js
//  Description: User Config Details.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ================================================================================================
// ** User List Component
import Table from './Table'
import { useTranslation } from 'react-i18next'


// ** Styles
import '@styles/react/apps/app-users.scss'
import '@styles/react/libs/tables/react-dataTable-component.scss'
import Breadcrumbs from '@components/breadcrumbs/bread'


const UsersList = () => {
  const {t} = useTranslation()
  return (
    <div className='app-user-list'>
      <Breadcrumbs breadCrumbTitle={t('User Management')}/>
      <Table />
    </div>
  )
}

export default UsersList
