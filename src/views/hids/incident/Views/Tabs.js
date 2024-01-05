// ================================================================================================
//  File Name: Tab.js
//  Description: Details of the HIDS Incident Graph.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { Nav, NavItem, NavLink } from 'reactstrap'
import { useTranslation } from 'react-i18next'

const Tabs = ({ activeTab, toggleTab }) => {
  const {t} = useTranslation()
  return (
    <Nav className='nav-inline' pills>
      <NavItem>
        <NavLink active={activeTab === '1'} onClick={() => toggleTab('1')}>
          <span className='font-weight-bold'>{t('Security Events')}</span>
        </NavLink>
      </NavItem>
      <NavItem>
        <NavLink active={activeTab === '2'} onClick={() => toggleTab('2')}>
          <span className='font-weight-bold'>{t('Mitre Att&ck')}</span>
        </NavLink>
      </NavItem>
    </Nav>
  )
}

export default Tabs
