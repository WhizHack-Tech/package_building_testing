// ================================================================================================
//  File Name: Tabs.js
//  Description: Details of the Edit Account Pages.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { Nav, NavItem, NavLink } from 'reactstrap'
import { useContext } from 'react'
import { User, Lock, Info, Link, Bell } from 'react-feather'
import { useTranslation } from 'react-i18next'
import { AbilityContext } from '@src/utility/context/Can'
const Tabs = ({ activeTab, toggleTab }) => {
  const { t } = useTranslation()
  const ability = useContext(AbilityContext)
  return (
    <Nav className='nav-left' pills vertical>
      <NavItem>
        <NavLink active={activeTab === '1'} onClick={() => toggleTab('1')}>
          <User size={18} className='mr-1' />
          <span className='font-weight-bold'>{t('General')}</span>
        </NavLink>
      </NavItem>
      {ability.can('read', 'all') ? (
        <NavItem>
          <NavLink active={activeTab === '3'} onClick={() => toggleTab('3')}>
            <Bell size={18} className='mr-1' />
            <span className='font-weight-bold'>{t('Notification')}</span>
          </NavLink>
        </NavItem>
      ) : null}
      <NavItem>
        <NavLink active={activeTab === '4'} onClick={() => toggleTab('4')}>
          <Info size={18} className='mr-1' />
          <span className='font-weight-bold'>{t('Information')}</span>
        </NavLink>
      </NavItem>
      {ability.can('read', 'all') ? (
        <NavItem>
          <NavLink active={activeTab === '5'} onClick={() => toggleTab('5')}>
            <Lock size={18} className='mr-1' />
            <span className='font-weight-bold'>{t('Config')}</span>
          </NavLink>
        </NavItem>
      ) : null}
    
      <NavItem>
        <NavLink active={activeTab === '6'} onClick={() => toggleTab('6')}>
          <Info size={18} className='mr-1' />
          <span className='font-weight-bold'>{t('Whitelists')}</span>
        </NavLink>
      </NavItem>
    </Nav>
  )
}

export default Tabs
