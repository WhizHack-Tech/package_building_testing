// =============================================================================================
//  File Name: horizontal-menu\index.js
//  Description: Details of the horizontal-menu component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

// ** React Imports
import { useState } from 'react'

// ** Horizontal Menu Array
import navigation from '@src/navigation/horizontal'

// ** Horizontal Menu Components
import HorizontalNavMenuItems from './HorizontalNavMenuItems'
import { useSelector } from "react-redux"
import { Link, useLocation } from 'react-router-dom'
import { Gitlab } from 'react-feather'
import { useTranslation } from 'react-i18next'
import { Spinner } from 'reactstrap'

const HorizontalMenu = ({ currentActiveItem, routerProps }) => {
  const { t } = useTranslation()
  // ** States
  const [activeItem, setActiveItem] = useState(null)
  const [groupActive, setGroupActive] = useState([])
  const [openDropdown, setOpenDropdown] = useState([])
  const pagePermissionStore = useSelector((store) => store.pagesPermissions)
  const path = useLocation()

  // ** On mouse enter push the ID to openDropdown array
  const onMouseEnter = id => {
    const arr = openDropdown
    arr.push(id)
    setOpenDropdown([...arr])
  }

  // ** On mouse leave remove the ID to openDropdown array
  const onMouseLeave = id => {
    const arr = openDropdown
    arr.splice(arr.indexOf(id), 1)
    setOpenDropdown([...arr])
  }

  const ExtenalLink = () => {

    return (
      <>
        {/* {pagePermissionStore.env_trace === true ? <li className={path.pathname === "/third-party/trace" ? 'nav-item active' : 'nav-item'}>
          <Link className='d-flex align-items-center' to="/third-party/trace" onClick={() => { setActiveItem("/third-party/trace") }}>
            <Gitlab size={20} />
            <span className='menu-title text-truncate'>{t('Trace')}</span>
          </Link>
        </li> : null}

        {pagePermissionStore.env_wazuh === true ? <li className={path.pathname === "/third-party/wazuh" ? 'nav-item active' : 'nav-item'}>
          <Link className='d-flex align-items-center' to="/third-party/wazuh" onClick={() => { setActiveItem("/third-party/wazuh") }}>
            <Gitlab size={20} />
            <span className='menu-title text-truncate'>{t('Endpoint Security')}</span>
          </Link>
        </li> : null} */}
      </>
    )
  }

  let pageGroupsName = {
    dashboard: true,
    administartion: true,
    report: true
  }

  const LoadingMenu = () => {
    if (pagePermissionStore.loading) {

      pageGroupsName = { ...pageGroupsName, ...pagePermissionStore } 

      return (
        <ul className='nav navbar-nav' id='main-menu-navigation'>
          <HorizontalNavMenuItems
            submenu={false}
            items={navigation(pageGroupsName)}
            activeItem={activeItem}
            groupActive={groupActive}
            routerProps={routerProps}
            onMouseEnter={onMouseEnter}
            onMouseLeave={onMouseLeave}
            openDropdown={openDropdown}
            setActiveItem={setActiveItem}
            setGroupActive={setGroupActive}
            setOpenDropdown={setOpenDropdown}
            currentActiveItem={currentActiveItem}
          />
          {/* <ExtenalLink /> */}
        </ul>
      )

    } else {
      return (
        <ul className='navigation navigation-main'>
          <li className='nav-item text-center mt-5'>
            <div className=''>
              <Spinner color='primary' />
            </div>
          </li>
        </ul>
      )
    }
  }

  return (
    <div className='navbar-container main-menu-content'>
      <LoadingMenu />
    </div>
  )
}

export default HorizontalMenu
