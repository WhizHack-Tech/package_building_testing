// ================================================================================================
//  File Name: Tabs2.js
//  Description: Details of the Edit Account Pages.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { Nav, NavItem, NavLink } from 'reactstrap'
import { useTranslation } from 'react-i18next'
const Tabs = ({ activeTab, toggleTab }) => {
  const { t } = useTranslation()
  return (
    <Nav className='nav-inline' pills>
      <NavItem className='mr-1'>
        <NavLink active={activeTab === '1'} onClick={() => toggleTab('1')}>
          <span className='font-weight-bold'>{t('Email Config')}</span>
        </NavLink>
      </NavItem>
      <NavItem>
        <NavLink active={activeTab === '2'} onClick={() => toggleTab('2')}>
          <span className='font-weight-bold'>{t('Notification Config')}</span>
        </NavLink>
      </NavItem> 
      <NavItem>
        <NavLink active={activeTab === '3'} onClick={() => toggleTab('3')}>
          <span className='font-weight-bold'>{t('Dashboard Config')}</span>
        </NavLink>
      </NavItem>
    </Nav>
  )
}

export default Tabs
