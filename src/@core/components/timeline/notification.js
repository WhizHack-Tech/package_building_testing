// =============================================================================================
//  File Name: timeline/notification.js
//  Description: Details of the notification component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

// ** Third Party Components
import Proptypes from 'prop-types'
import classnames from 'classnames'

const Timeline = props => {
  // ** Props
  const { data, tag, className } = props

  // ** Custom Tagg
  const Tag = tag ? tag : 'ul'

  return (
    <Tag
      className={classnames('timeline', {
        [className]: className
      })}
    >
      {data.map((item, i) => {
        const ItemTag = item.tag ? item.tag : 'li'

        return (
          <ItemTag
            key={i}
            className={classnames('timeline-item', {
              [item.className]: className
            })}
          >
            <span
              className={classnames('timeline-point', {
                [`timeline-point-${item.color}`]: item.color,
                'timeline-point-indicator': !item.icon
              })}
            >
              {item.icon ? item.icon : null}
            </span>
            <div className='timeline-event'>
                <p>Threat Type : <b className='text-warning'>{item.title}</b></p>
                <p>Target IP : <b>{item.target_ip}</b></p>
                <p>Target Mac : <b>{item.target_mac}</b></p>
                <p>Attacker IPs : <b>{item.attacker_ip}</b></p>
                <p>Attacker Mac : <b>{item.attacker_mac}</b></p>
                <p>Count : <b className='text-danger'>{item.counts}</b></p>
            </div>
          </ItemTag>
        )
      })}
    </Tag>
  )
}

export default Timeline

// ** PropTypes
Timeline.propTypes = {
  data: Proptypes.array.isRequired,
  className: Proptypes.string,
  tag: Proptypes.string
}
