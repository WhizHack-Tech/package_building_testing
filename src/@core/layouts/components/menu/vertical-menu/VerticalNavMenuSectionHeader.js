// ==============================================================================================
//  File Name: VerticalNavMenuSectionHeader.js
//  Description: Details of the VerticalNavMenuSectionHeader component.
//  ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

// ** Third Party Components
import { MoreHorizontal } from 'react-feather'

const VerticalNavMenuSectionHeader = ({ item, index }) => {
  return (
    <li className='navigation-header'>
      <span>{item.header}</span>
      <MoreHorizontal className='feather-more-horizontal' />
    </li>
  )
}

export default VerticalNavMenuSectionHeader
