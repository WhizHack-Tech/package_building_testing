// ================================================================================================
//  File Name: index.js
//  Description: Details of the Administration ( List User Details ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// =============================================================================================
// // ** User List Component
import { Fragment } from 'react'
import TableWithButtons from './TableWithButtons'
import BreadCrumbs from '@components/breadcrumbs'

// ** Styles
import '@styles/react/apps/app-users.scss'
import '@styles/react/libs/tables/react-dataTable-component.scss'

const UsersList = () => {
  return (
    <Fragment>
<BreadCrumbs breadCrumbTitle='User Config Details'/>
    <div className='app-user-list'>
      <TableWithButtons />
    </div>
  </Fragment>
  )
}

export default UsersList
