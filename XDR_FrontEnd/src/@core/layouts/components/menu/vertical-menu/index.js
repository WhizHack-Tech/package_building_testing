// =============================================================================================
//  File Name: vertical-menu\index.js
//  Description: Details of the vertical-menu component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

// ** React Imports
import { Fragment, useState, useRef } from 'react'

// ** Vertical Menu Items Array
import Navigation from '@src/navigation/vertical'

// ** Third Party Components
import classnames from 'classnames'
import PerfectScrollbar from 'react-perfect-scrollbar'

// ** Vertical Menu Components
import VerticalMenuHeader from './VerticalMenuHeader'
import VerticalNavMenuItems from './VerticalNavMenuItems'
import { Link, useLocation } from 'react-router-dom'
import { Gitlab } from 'react-feather'
import { useSelector } from "react-redux"
import { useTranslation } from 'react-i18next'
import { Spinner } from 'reactstrap'
const Sidebar = props => {
  const { t } = useTranslation()
  // ** Props
  const { menuCollapsed, routerProps, menu, currentActiveItem, skin } = props
  const pagePermissionStore = useSelector((store) => store.pagesPermissions)
  // const path = useLocation()
  // ** States
  const [groupOpen, setGroupOpen] = useState([])
  const [groupActive, setGroupActive] = useState([])
  const [activeItem, setActiveItem] = useState(null)

  // ** Menu Hover State
  const [menuHover, setMenuHover] = useState(false)

  // ** Ref
  const shadowRef = useRef(null)

  // ** Function to handle Mouse Enter
  const onMouseEnter = () => {
    if (menuCollapsed) {
      setMenuHover(true)
    }
  }

  // ** Scroll Menu
  const scrollMenu = container => {
    if (shadowRef && container.scrollTop > 0) {
      if (!shadowRef.current.classList.contains('d-block')) {
        shadowRef.current.classList.add('d-block')
      }
    } else {
      if (shadowRef.current.classList.contains('d-block')) {
        shadowRef.current.classList.remove('d-block')
      }
    }
  }

  const ExtenalLink = () => {

    return (
      <>
        {/* {(pagePermissionStore.env_trace === true || pagePermissionStore.env_wazuh === true) ? <li class="navigation-header"><span>{t('Plugin')}</span></li> : null}

        {pagePermissionStore.env_trace === true ? <li className={path.pathname === "/third-party/trace" ? 'nav-item active' : 'nav-item'}>
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
        <ul className='navigation navigation-main'>
          <VerticalNavMenuItems
            items={Navigation(pageGroupsName)}
            groupActive={groupActive}
            setGroupActive={setGroupActive}
            activeItem={activeItem}
            setActiveItem={setActiveItem}
            groupOpen={groupOpen}
            setGroupOpen={setGroupOpen}
            routerProps={routerProps}
            menuCollapsed={menuCollapsed}
            menuHover={menuHover}
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
    <Fragment>
      <div
        className={classnames('main-menu menu-fixed menu-accordion menu-shadow', {
          expanded: menuHover || menuCollapsed === false,
          'menu-light': skin !== 'semi-dark' && skin !== 'dark',
          'menu-dark': skin === 'semi-dark' || skin === 'dark'
        })}
        onMouseEnter={onMouseEnter}
        onMouseLeave={() => setMenuHover(false)}
      >
        {menu ? (
          menu
        ) : (
          <Fragment>
            {/* Vertical Menu Header */}
            <VerticalMenuHeader setGroupOpen={setGroupOpen} menuHover={menuHover} {...props} />
            {/* Vertical Menu Header Shadow */}
            <div className='shadow-bottom' ref={shadowRef}></div>
            {/* Perfect Scrollbar */}
            <PerfectScrollbar
              className='main-menu-content'
              options={{ wheelPropagation: false }}
              onScrollY={container => scrollMenu(container)}
            >
              <LoadingMenu />
            </PerfectScrollbar>
          </Fragment>
        )}
      </div>
    </Fragment>
  )
}

export default Sidebar