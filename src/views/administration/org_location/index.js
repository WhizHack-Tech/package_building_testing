// ================================================================================================
//  File Name: index.js
//  Description: Details of the Administration ( Add Organization Location Details ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
// ** React Imports
import { useRef, useState } from 'react'

// ** Custom Components
import Wizard from '@components/wizard'

import BasicDetails from "./basicDetails"
import ProductDetails from './productDetails'
import License from './license'
import Config from './congifDetails'

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
      id: 'product_details',
      title: 'Product Details',
      subtitle: 'Enter Your Product Details.',
      content: <ProductDetails stepper={stepper} />
    },
    {
      id: 'config_details',
      title: 'Config Setting',
      subtitle: 'Add Your Config Details.',
      content: <Config stepper={stepper} />
    },
    {
      id: 'license_details',
      title: 'License Management',
      subtitle: 'Enter Your Product Details.',
      content: <License stepper={stepper} />
    }
  ]

  return (
    <div className='horizontal-wizard'>
      <Wizard instance={el => setStepper(el)} ref={ref} steps={steps} />
    </div>
  )

}

export default AttachOrgToLocation