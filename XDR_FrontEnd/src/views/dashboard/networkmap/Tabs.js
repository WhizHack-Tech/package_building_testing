import { Nav, NavItem, NavLink } from 'reactstrap'
import { useTranslation } from 'react-i18next'

const Tabs = ({ activeTab, toggleTab }) => {
  const { t } = useTranslation()
  return (
    <Nav className='nav-inline' pills>
      <NavItem>
        <NavLink active={activeTab === '1'} onClick={() => toggleTab('1')}>
          <span className='font-weight-bold'>{t('On-Prim')}</span>
        </NavLink>
      </NavItem>
      <NavItem>
        <NavLink active={activeTab === '3'} onClick={() => toggleTab('3')}>
          <span className='font-weight-bold'>{t('AWS')}</span>
        </NavLink>
      </NavItem>
    </Nav>
  )
}

export default Tabs
