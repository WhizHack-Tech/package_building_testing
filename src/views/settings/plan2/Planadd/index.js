// ================================================================================================
//  File Name: index.js
//  Description: Details of the Setting ( Plan Add ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// =============================================================================================
// ** React Imports
import { useRef, useState } from 'react'

// ** Custom Components
import Wizard from '@components/wizard'

import BasicDetails from "./basicDetails"
import Defalut from "./defalutpages"
import Lisence from './Lisences'

const AttachOrgToLocation = () => {
  // ** Ref
  const ref = useRef(null)

  // ** State
  const [stepper, setStepper] = useState(null)

  const steps = [
    {
      id: 'basic_details',
      title: 'Basic Details',
      subtitle: 'Enter Your Basic Details.',
      content: <BasicDetails stepper={stepper} />
    },
    {
      id: 'defalut_details',
      title: 'Defalut Page',
      subtitle: 'Enter Your Defalut Page Details.',
      content: <Defalut stepper={stepper} />
    },
    {
      id: 'lisence_details',
      title: 'License Management',
      subtitle: 'Enter Your License Management Details.',
      content: <Lisence stepper={stepper} />
    }

  ]

  return (
    <div className='horizontal-wizard'>
      <Wizard instance={el => setStepper(el)} ref={ref} steps={steps} />
    </div>
  )

}

export default AttachOrgToLocation