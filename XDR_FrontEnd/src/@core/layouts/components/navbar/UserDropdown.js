// =============================================================================================
//  File Name: UserDropdown.js
//  Description: Details of the UserDropdown component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

// ** React Imports
import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
// ** Custom Components
import Avatar from '@components/avatar'

// ** Utils
import { isUserLoggedIn } from '@utils'

// ** Store & Actions
import { useDispatch, useSelector } from 'react-redux'
import { handleLogout } from '@store/actions/auth'

// ** Third Party Components
import { UncontrolledDropdown, DropdownMenu, DropdownToggle, DropdownItem } from 'reactstrap'
import { User, Power } from 'react-feather'

const UserDropdown = () => {
  // ** Store Vars
  const {t} = useTranslation()
  const dispatch = useDispatch()
  const UpdateUserData = useSelector(store => store.auth.userData)
  
  // ** State
  const [userData, setUserData] = useState(null)

  //** ComponentDidMount
  useEffect(() => {
    if (isUserLoggedIn() !== null) {
      setUserData(JSON.parse(localStorage.getItem('clientData')))
    }
  }, [])

  useEffect(() => {
    setUserData(JSON.parse(localStorage.getItem('clientData')))
  }, [UpdateUserData.first_name, UpdateUserData.profile_photo_path])

  return (
    <UncontrolledDropdown tag='li' className='dropdown-user nav-item'>
      <DropdownToggle href='/' tag='a' className='nav-link dropdown-user-link' onClick={e => e.preventDefault()}>
        <div className='user-nav d-sm-flex d-none'>
          <span className='user-name font-weight-bold'>{(userData && userData['first_name'])}</span>
          <span className='user-status'>{(userData && userData.role) || 'Admin'}</span>
        </div>
        {(userData && userData.profile_photo_path !== undefined && userData.profile_photo_path !== null) ? <Avatar img={`${userData.profile_photo_path}`} imgHeight='40' imgWidth='40' status='online' /> : <Avatar color={'primary'} className='mr-1' imgHeight='40' imgWidth='40' status='online' content={(userData && userData['first_name']) ? userData['first_name'] : "" } initials />}
      </DropdownToggle>
      <DropdownMenu right>
        <DropdownItem tag={Link} to='/settings/editaccount'>
          <User size={14} className='mr-75' />
          <span className='align-middle'>{t('Profile')}</span>
        </DropdownItem>
        <DropdownItem tag={Link} to='/login' onClick={() => dispatch(handleLogout())}>
          <Power size={14} className='mr-75' />
          <span className='align-middle'>{t('Logout')}</span>
        </DropdownItem>
      </DropdownMenu>
    </UncontrolledDropdown>
  )
}

export default UserDropdown
