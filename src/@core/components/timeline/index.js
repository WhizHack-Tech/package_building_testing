// =============================================================================================
//  File Name: timeline/index.js
//  Description: Details of the timeline component.
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
              <div
                className={classnames('d-flex justify-content-between flex-sm-row flex-column', {
                  'mb-sm-0 mb-1': item.meta
                })}
              >
                <h6>{item.title}</h6>
                {item.meta ? (
                  <span
                    className={classnames('timeline-event-time', {
                      [item.metaClassName]: item.metaClassName
                    })}
                  >
                    {item.meta}
                  </span>
                ) : null}
              </div>
              <p className={classnames({'mb-0': i === data.length - 1 && !item.customContent})}
              >
                <div>{item.content}</div>
              </p>
              {item.customContent ? item.customContent : null}
              <p
                className={classnames({
                  'mb-1': i === data.length - 1 && !item.type
                })}
              >
                {item.method}
              </p>
              {item.type ? item.type : null}
              <p
                className={classnames({
                  'mb-0': i === data.length - 1 && !item.customContent
                })}
              >
                {item.username}
              </p>
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
