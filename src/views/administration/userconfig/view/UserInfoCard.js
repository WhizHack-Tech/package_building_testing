// ================================================================================================
//  File Name:  UserinfoCard.js
//  Description: User Config Details.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ================================================================================================

// ** React Imports
import { Fragment } from 'react'
import { Link } from 'react-router-dom'
import { Card, CardBody, Button, Badge, Spinner } from 'reactstrap'
import Avatar from '@components/avatar'
import { staticPath } from '@axios'
import '@styles/react/libs/react-select/_react-select.scss'
import { useTranslation } from 'react-i18next'

const roleColors = {
  editor: 'light-info',
  admin: 'light-danger',
  author: 'light-warning',
  maintainer: 'light-success',
  subscriber: 'light-primary'
}


const UserInfoCard = ({ selectedUser }) => {
  const {t} = useTranslation()
  if (selectedUser === null) {
    return <div className='d-flex justify-content-center'><Spinner color='primary' type='grow' /></div>
  }
  // ** render user img
  const renderUserImg = () => {
    if (selectedUser.profile_photo !== null) {
      return (
        <img
          height='110'
          width='110'
          alt='user-avatar'
          src={`${selectedUser.profile_photo}`}
          className='img-fluid rounded mt-3 mb-2'
        />
      )
    } else {
      const stateNum = Math.floor(Math.random() * 6),
        states = ['light-success', 'light-danger', 'light-warning', 'light-info', 'light-primary', 'light-secondary'],
        color = states[stateNum]
      return (
        <Avatar
          initials
          color={color}
          className='rounded mt-3 mb-2'
          content={selectedUser.first_name}
          contentStyles={{
            borderRadius: 0,
            fontSize: 'calc(48px)',
            width: '100%',
            height: '100%'
          }}
          style={{
            height: '110px',
            width: '110px'
          }}
        />
      )
    }
  }


  return (
    <Fragment>
      <Card>
        <CardBody>
          <div className='user-avatar-section'>
            <div className='d-flex align-items-center flex-column'>
              {renderUserImg()}
              <div className='d-flex flex-column align-items-center text-center'>
                <div className='user-info'>
                  <h2>{selectedUser !== null ? selectedUser.first_name : 'Eleanor Aguilar'} {selectedUser !== null ? selectedUser.last_name  : 'Eleanor Aguilar'}</h2>
                  {selectedUser !== null ? (
                    <Badge color={roleColors[selectedUser.first_name]} className='text-capitalize'>
                      {selectedUser.role}
                    </Badge>
                  ) : null}
                </div>
              </div>
            </div>
          </div>
          <h2 className='fw-bolder border-bottom pb-50 mb-1'>{t('Details')}</h2>
          <div className='info-container'>
            {selectedUser !== null ? (
              <ul className='list-unstyled'>
                <li className='mb-75'>
                  <span className='fw-bolder me-25'>{t('Email')} : </span>
                  <span>{selectedUser.email}</span>
                </li>
                <li className='mb-75'>
                  <span className='fw-bolder me-25'>{t('Country')} : </span>
                  <span className='text-capitalize'>{selectedUser.country}</span>
                </li>
                <li className='mb-75'>
                  <span className='fw-bolder me-25'>{t('Contact')} : </span>
                  <span>{selectedUser.contact_number}</span>
                </li>
              </ul>
            ) : null}
          </div>
        </CardBody>
      </Card>
    </Fragment>
  )
}

export default UserInfoCard
