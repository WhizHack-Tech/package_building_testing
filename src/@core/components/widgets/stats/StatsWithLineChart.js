// =============================================================================================
//  File Name: widgets\stats\StatsWithLineChart.js
//  Description: Details of the stats StatsWithLineChart component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

// ** Custom Components
import Avatar from '@components/avatar'

// ** Third Party Components
import PropTypes from 'prop-types'
import Chart from 'react-apexcharts'
import { Card, CardHeader, CardText } from 'reactstrap'

// ** Default Options
import { lineChartOptions } from './ChartOptions'

const StatsWithLineChart = ({ icon, color, stats, statTitle, series, options, type, height, ...rest }) => {
  
  return (
    <Card {...rest}>
      <CardHeader className='align-items-start pb-0'>
        <div>
          <h2 className='font-weight-bolder'>{stats}</h2>
          <CardText>{statTitle}</CardText>
        </div>
        <span>
           {icon}
        </span>
        {/* <color={`light-${color}`} icon={icon} /> */}
      </CardHeader>
      <Chart options={options} series={series} type={type} height={height ? height : 100} />
    </Card>
  )
}

export default StatsWithLineChart

// ** PropTypes
StatsWithLineChart.propTypes = {
  icon: PropTypes.element.isRequired,
  color: PropTypes.string.isRequired,
  stats: PropTypes.string.isRequired,
  statTitle: PropTypes.string.isRequired,
  options: PropTypes.object,
  series: PropTypes.array.isRequired,
  type: PropTypes.string,
  height: PropTypes.string
}

// ** Default Props
StatsWithLineChart.defaultProps = {
  options: lineChartOptions,
  color: 'primary'
}
