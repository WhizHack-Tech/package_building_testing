// ================================================================================================
//  File Name: awsMap.js
//  Description: Details of the Network Map.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import React, { createRef } from 'react'
import Tree from "react-d3-tree"
import { Card, CardBody } from 'reactstrap'
import { FullScreen, useFullScreenHandle } from "react-full-screen"
import { Maximize } from 'react-feather'
import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import "./graphStyle.css"
import "./globalCss.css"

const AwsMap = ({ awsData }) => {
  const { t } = useTranslation()
  const handle = useFullScreenHandle()

  const containerStyles = {
    width: "100%",
    height: "100vh"
  }

  const renderNodeWithCustomEvents = ({ nodeDatum, toggleNode, wrapper }) => {
    // Horizontal orientation
    let y = 18
    // let y = -25;
    let x = -5

    return (
      <g ref={wrapper}>
        {/* <Tooltip
        title={<Typography>{nodeDatum.name}</Typography>}
        arrow
        placement="right"
      > */}
        <arrow fill="#968df4"></arrow>
        <circle
          r="6"
          fill={nodeDatum.children ? "#ff9f43" : "#fb255e"}
          onClick={
            nodeDatum.children ? toggleNode : () => {
              console.log(nodeDatum)
            }
          }
        />
        {/* </Tooltip> */}
        <stoke fill="#968df4"></stoke>
        <text fill="#968df4" strokeWidth="0.1" fontSize="10px" x={x.toString()} y={y.toString()}>
          {nodeDatum.name}
        </text>
      </g>
    )
  }

  // const [translate, containerRef] = useCenteredTree();
  const wrapper = createRef()
  return (
    <Card>
      <div className='content-header-right text-md-left '>
        <Link color='primary' onClick={handle.enter} >
          <Maximize size={30} /> {t("Fullscreen")}
        </Link>
      </div>
      <FullScreen handle={handle}>
        <div>
          <CardBody>
            <div style={containerStyles}>
              {awsData.length > 0 ? <Tree
                data={awsData[0]}
                collapsible={true}
                enableLegacyTransitions={true}
                initialDepth={"5"}
                orientation="horizontal"
                depthFactor="200"
                translate={{ x: 200, y: 300 }}
                shouldCollapseNeighborNodes={false}
                nodeSize={{ y: 30 }}
                // translate={translate}
                renderCustomNodeElement={(props) => renderNodeWithCustomEvents({ ...props, wrapper })
                }

              /> : <p className='data-not-fount'>{t("Data not available at this moment")}</p>}
            </div>
          </CardBody>
        </div>
      </FullScreen>
    </Card>
  )
}

export default AwsMap