// =============================================================================================
//  File Name: VerticalNavMenuSectionHeader.js
//  Description: Details of the Vertical Nav Menu Section Header component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

// ** Third Party Components
import { Fragment } from 'react'
import { MoreHorizontal } from 'react-feather'
import { useTranslation } from 'react-i18next'

const VerticalNavMenuSectionHeader = ({ item, index }) => {
  const { t } = useTranslation()

  return (
    <Fragment>
    <li className='navigation-header d-flex align-items-center'>
     <span>
     {
        item.imageIcon ? <img src={item.imageIcon} style={
          {
            height: '34.47px',
            width: '37px',
            marginRight: '5px',
            marginLeft:'-10px'
          }
        } /> : null
      }

      {
        item.icon ? item.icon : null
      }
     </span>
      <span>{t(item.header)}</span>
      <MoreHorizontal className='feather-more-horizontal' />
    </li>
    </Fragment>
  )
}

export default VerticalNavMenuSectionHeader
