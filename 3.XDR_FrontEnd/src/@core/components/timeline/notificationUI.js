// =============================================================================================
//  File Name: timeline/notificationUI.js
//  Description: Details of the notificationUI component.
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
              {item.objKey.map((val, inx) => (
                <p key={i + inx}>{val} : <b className='text-warning'>{JSON.stringify(item.objVal[inx])}</b></p>
              ))}
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
