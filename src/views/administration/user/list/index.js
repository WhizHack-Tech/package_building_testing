// ================================================================================================
//  File Name: index.js
//  Description: Details of the Administration ( View Organization Details ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ===========================================================================================
// ** React Imports
import { Fragment, useEffect, useState } from 'react'
import BreadCrumbs from '@components/breadcrumbs'
import { useDispatch, useSelector } from 'react-redux'
// ** Third Party Components
import TableWithButtons from './TableWithButtons'
import { getAllData } from '../store/action'


// ** Styles
import '@styles/react/apps/app-users.scss'
import '@styles/react/libs/tables/react-dataTable-component.scss'

const UsersList = () => {
  const dispatch = useDispatch()
  const [checkUpdate, setCheckUpdate] = useState('active')
  
  return (
    <Fragment>
      <BreadCrumbs breadCrumbTitle='Organization Details' />
      <div className='app-user-list'>
        <TableWithButtons />
      </div>
    </Fragment>
  )
}

export default UsersList
