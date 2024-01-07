// =============================================================================================
//  File Name: NavbarBookmarks.js
//  Description: Details of the Navbar Bookmarks component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { Fragment, useState } from 'react'
import { Button, Modal, ModalHeader, ModalBody, ModalFooter, Alert } from 'reactstrap'
// import img from '@src/assets/images/banner/banner-6.jpg'
import '@styles/react/apps/app-email.scss'

    const ModalConfig = [
      {
        id: 1,
        btnTitle: 'Manual Installation',
        modalTitle: 'Manual Installation ',
        modalClass: 'modal-lg'
      }
    ]
const ModalSizes = () => {
        const [modal, setModal] = useState(null)
        const toggleModal = id => {
            if (modal !== id) {
              setModal(id)
            } else {
              setModal(null)
            }
          }
          // const steps = [
          //   {
          //     id: 'CardTitle',
          //     title: 'Card',
          //     text: 'This is a card',
          //     attachTo: { element: '#tour .CardTitle', on: 'left' },
          //     cancelIcon: {
          //       enabled: true
          //     },
          //     buttons: [
          //       {
          //         text: 'Skip',
          //         classes: backBtnClass,
          //         action: () => instance.cancel()
          //       },
          //       {
          //         text: 'Back',
          //         classes: backBtnClass,
          //         action: () => instance.back()
          //       },
          //       {
          //         text: 'Next',
          //         classes: nextBtnClass,
          //         action: () => instance.next()
          //       }
          //     ]
          //   }
          // ]
    const renderModal = ModalConfig.map(item => {
    return (
<Fragment key={item.id}>
          <div>
            <Button.Ripple color='primary' onClick={() => toggleModal(item.id)} key={item.title} outline size='sm'>
            {item.btnTitle}
            </Button.Ripple>
          </div>
    <Modal
      isOpen={modal === item.id}
      toggle={() => toggleModal(item.id)}
      className={`modal-dialog-centered ${item.modalClass}`}
      key={item.id}
     >
     <div className='scroll-box'>
          <ModalHeader toggle={() => toggleModal(item.id)}>
            <h2>{item.modalTitle}</h2>
            {item.title}
            </ModalHeader>
                <ModalBody>
                <h5>The manual xdr installation is performed in two steps.</h5>
                The first step requires installation of xdr package from the official repository by using a single command and the second step requires configuration of the package by using the xdr management commands. Follow this step-by-step guide for performing a manual xdr installation on your server.
                <h5 className='mt-1'>Step-by-Step Guide.</h5>
                <p>I assume here that you have a base Debian 11 machine ready on which you are going to install the package. The machine must have access to the internet during the installation is being performed. On the terminal login with your user and follow these steps.</p>
                <h5>1. Download and Install the xdr package by using the following command. </h5>
                <Alert className='mt-1' color='success'>
                <div className='alert-body' id="link">curl --proto '=https' --tlsv1.2 -sSf https://get.zerohack.in/zh-xdr-repo/install.sh | sh </div>
                </Alert>
                {/* <h6><img src={img} width="250px" height="250px"/> </h6> <br /> */}
                <h5>2. After the download finishes you need to follow the below steps to start configuration of the xdr software.</h5> <br />
                <p>2.1. To start initial configurations of the xdr honeynet enter the command from a sudo user account (preferrably root itself.)</p>
                <Alert color='success'>
                <div className='alert-body'>xdr -i</div> 
                </Alert> 
                <p>2.2 This command will prompt you to enter several licensing information that you have acquired from the zerohack team via email these details are listed below.</p> <br />
                <Alert color='primary'>
                <div className='alert-body' id="index">Your index name</div> 
                </Alert> 
                <Alert color='primary'>
                <div className='alert-body'>Your bucket ID</div> 
                </Alert>
                <Alert color='primary'>
                <div className='alert-body'>Your access key ID</div> 
                </Alert>
                <Alert color='primary'>
                <div className='alert-body'>Your secret access key</div> 
                </Alert> 
                <Alert color='primary'>
                <div className='alert-body'>The default region</div> 
                </Alert>
                <Alert color='primary'>
                <div className='alert-body'>Your choice of honeynet to install</div>
                </Alert>
                <Alert color='warning'>
                <div className='alert-body'>Note: In case you do not have this information you need to mail us at info@whizhack.com</div>
                </Alert>
                <p>2.3. After the installation is complete you need to reboot the virtual machines for the software to work correctly.</p>
                <p>2.4. Following is an example of how you can fill your details for xdr -i command. </p> <br />
                {/* <img src={img} width="250px" height="250px"/> */}
          </ModalBody>
      </div>
         <ModalFooter>
          <Button color='primary' onClick={() => toggleModal(item.id)} outline>
           Done
          </Button>
        </ModalFooter>
   </Modal>
</Fragment>
    )
  })

return <div className='demo-inline-spacing'>{renderModal}</div>
}
export default ModalSizes
