// ==============================================================================================
//  File Name: UserDropdown.js
//  Description: Details of the UserDropdown component.
//  ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

// ** React Imports
import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

// ** Custom Components
import Avatar from '@components/avatar'

// ** Utils
import { isUserLoggedIn } from '@utils'

// ** Store & Actions
import { useDispatch } from 'react-redux'
import { handleLogout } from '@store/actions/auth'

// ** Third Party Components
import { UncontrolledDropdown, DropdownMenu, DropdownToggle, DropdownItem } from 'reactstrap'
import { User, Mail, CheckSquare, MessageSquare, Settings, CreditCard, HelpCircle, Power } from 'react-feather'

// ** Default Avatar Image
import defaultAvatar from '@src/assets/images/portrait/small/avatar-s-11.jpg'

const UserDropdown = () => {
  // ** Store Vars
  const dispatch = useDispatch()

  // ** State
  const [userData, setUserData] = useState('')

  //** ComponentDidMount
  useEffect(() => {
    if (isUserLoggedIn() !== null) {
      setUserData(JSON.parse(localStorage.getItem('userData')))
    }
  }, [])

  //** Vars
  // const userAvatar = (userData && userData.avatar) || defaultAvatar
  const renderClient = userData => {
    const stateNum = Math.floor(Math.random() * 6),
      states = ['light-success', 'light-danger', 'light-warning', 'light-info', 'light-primary', 'light-secondary'],
      color = states[stateNum]
  
    if (userData.avatar) {
      return <Avatar className='mr-1' img={userData.avatar} width='45' height='40' />
    } else {
      return <Avatar color={color || 'primary'} className='mr-1' content={userData.name || 'John Doe'} initials />
    }
  }

  return (
    <UncontrolledDropdown tag='li' className='dropdown-user nav-item'>
      <DropdownToggle href='/' tag='a' className='nav-link dropdown-user-link' onClick={e => e.preventDefault()}>
        <div className='user-nav d-sm-flex d-none'>
          <span className='user-name font-weight-bold'>{(userData && userData['name'])}</span>
          <span className='user-status'>{(userData && userData.role) || 'Admin'}</span>
        </div>
        {renderClient(userData)}
        {/* <Avatar img={userAvatar} imgHeight='40' imgWidth='40' status='online' /> */}
      </DropdownToggle>
      <DropdownMenu right>
        {/* <DropdownItem tag={Link} to='/settings/editaccount'>
          <User size={14} className='mr-75' />
          <span className='align-middle'>Profile</span>
        </DropdownItem> */}
        {/* <DropdownItem tag={Link} to='#' onClick={e => e.preventDefault()}>
          <Mail size={14} className='mr-75' />
          <span className='align-middle'>Inbox</span>
        </DropdownItem> */}
        {/* <DropdownItem tag={Link} to='#' onClick={e => e.preventDefault()}>
          <CheckSquare size={14} className='mr-75' />
          <span className='align-middle'>Tasks</span>
        </DropdownItem> */}
        {/* <DropdownItem tag={Link} to='#' onClick={e => e.preventDefault()}>
          <MessageSquare size={14} className='mr-75' />
          <span className='align-middle'>Chats</span>
        </DropdownItem> */}
        <DropdownItem tag={Link} to='/login' onClick={() => dispatch(handleLogout())}>
          <Power size={14} className='mr-75' />
          <span className='align-middle'>Logout</span>
        </DropdownItem>
      </DropdownMenu>
    </UncontrolledDropdown>
  )
}

export default UserDropdown
