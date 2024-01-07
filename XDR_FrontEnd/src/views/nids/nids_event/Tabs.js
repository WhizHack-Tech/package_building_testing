
// ================================================================================================
//  File Name: Tab.js
//  Description: Details of the NIDS Events ( Tabs )
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { Nav, NavItem, NavLink } from 'reactstrap'
import { useTranslation } from 'react-i18next'

const Tabs = ({ activeTab, toggleTab }) => {
  const { t } = useTranslation()
  return (
    <Nav className='justify-content-center' pills>
      <NavItem>
        <NavLink active={activeTab === '2'} onClick={() => toggleTab('2')}>
          <span className='font-weight-bold'>{t('ML & DL Detection')}</span>
        </NavLink>
      </NavItem>
      <NavItem>
        <NavLink active={activeTab === '1'} onClick={() => toggleTab('1')}>
          <span className='font-weight-bold'>{t('Signature-Based Detection')}</span>
        </NavLink>
      </NavItem>
    </Nav>
  )
}

export default Tabs
