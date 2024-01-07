import React from "react"
import axios from "@axios"
import { token } from '@utils'
// Import Highcharts
import Highcharts from "highcharts/highstock"
import HighchartsReact from "highcharts-react-official"
import networkgraph from "highcharts/modules/networkgraph"
import { CardBody, Card } from "reactstrap"

if (typeof Highcharts === "object") {
  networkgraph(Highcharts)
}

Highcharts.addEvent(
    Highcharts.Series,
    'afterSetOptions',
    function (e) {
        const colors = Highcharts.getOptions().colors,
            i = 0,
            nodes = {}

        if (
            e instanceof Highcharts.seriesTypes.networkgraph &&
            e.options.id === 'lang-tree'
        ) {
            e.options.data.forEach(function (link) {

                if (link[0] === 'Proto Indo-European') {
                    nodes['Proto Indo-European'] = {
                        id: 'Proto Indo-European',
                        marker: {
                            radius: 10
                        }
                    }
                    nodes[link[1]] = {
                        id: link[1],
                        marker: {
                            radius: 10
                        },
                        color: colors[i++]
                    }
                } else if (nodes[link[0]] && nodes[link[0]].color) {
                    nodes[link[1]] = {
                        id: link[1],
                        color: nodes[link[0]].color
                    }
                }
            })

            e.options.nodes = Object.keys(nodes).map(function (id) {
                return nodes[id]
            })
        }
    }
)

class GraphChart extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      options: {
        chart: {
          type: "networkgraph",
          height: '50%'
        },
        title: {
          text: ""
        },
        plotOptions: {
          networkgraph: {
            keys: ["from", "to"],
            layoutAlgorithm: {
              enableSimulation: true,
              // linkLength: 50,
              // friction: -0.9,
              // integration: "verlet",
              // // approximation: "barnes-hut",
              // gravitationalConstant: 5
              friction: -0.9
            }
          }
        },
        series: [
          {   
            accessibility: {
                enabled: false
            },         
            marker: {
              radius: 3
            },
            dataLabels: {
              enabled: true,
              linkFormat: "",
              allowOverlap: false
            },
            id: 'lang-tree',
            data: []               
          }
        ]
      }
    }
  }

  componentDidMount() {
    this.UserList()
  }

  UserList() {
    axios.get('/aws-network-map',
    { headers: { Authorization: token() } })
    .then(res => {
      if (res.data.message_type === "success") {
        this.setState({options:{
            series:{
                data:res.data.data
            }
        }})
      } else {
        this.setState({options:{
          series:{
              data:[]
          }
      }})
      }

    })      
  }
  render() {
    return (
      <CardBody>  
            
        <HighchartsReact highcharts={Highcharts} options={this.state.options} />
      </CardBody>
    )
  }
}
export default GraphChart