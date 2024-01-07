// ================================================================================================
//  File Name: Animate.jsx
//  Description: Details of the Animate.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import React from "react"
import { Cloud } from "react-icon-cloud"

function App() {

  const containerProps = {
    style: {
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      width: "100%",
      paddingTop: 40
    }
  }

  const canvasProps = {
    shape: "circle"
  }


  const options = {
    // activateAudio: string
    // activeCursor: string
    // altImage: boolean
    // animTiming: 'Smooth' | 'Linear'
    // audioIcon: boolean
    // audioIconDark: boolean
    // audioIconSize: number
    // audioIconThickness: number
    // audioVolume: number
    // bgColor: null | string
    // bgOutlineThickness: number
    // bgRadius: number
    // centreFunc: any
    // centreImage: any
    clickToFront: 500,
    // decel: number
    depth: 1,
    // dragControl: boolean
    // dragThreshold: number
    // fadeIn: number
    // freezeActive: boolean
    // freezeDecel: boolean
    // frontSelect: boolean
    // hideTags: boolean
    // imageAlign: 'centre' | 'left' | 'right'
    // imageMode: null | 'image' | 'text' | 'both'
    // imagePadding: number
    // imagePosition: 'top' | 'bottom' | 'left' | 'right'
    // imageRadius: number | string
    imageScale: 2,
    // imageVAlign: 'top' | 'bottom' | 'middle'
    initial: [0.1, -0.1],
    // interval: number
    // lock: null | 'x' | 'y' | 'xy'
    // maxBrightness: number
    // maxSpeed: number
    // minBrightness: number
    // minSpeed: number
    // minTags: 0 - 200
    // noMouse: boolean
    // noSelect: boolean
    // noTagsMessage: string
    // offsetX: number
    // offsetY: number
    outlineColour: "#0000",
    // outlineDash: number
    // outlineDashSpace: number
    // outlineIncrease: number
    // outlineMethod: 'outline' | 'classic' | 'block' | 'colour' | 'size' | 'none'
    // outlineOffset: number
    // outlineRadius: number
    // outlineThickness: number
    // padding: number
    // pinchZoom: boolean
    // pulsateTime: number
    // pulstateTo: number
    // radiusX: number
    // radiusY: number
    // radiusZ: number
    // repeatTagsTags: 0 - 64
    reverse: true,
    // scrollPause: boolean
    // shadow: string
    // shadowBlur: number
    // shadowOffset: [number,number] | number[]
    // shape: 'sphere' | 'hcylinder' | 'vcylinder' | 'hring' | 'vring'
    // shuffleTags: boolean
    // splitWidth: number
    // stretchX: number
    // stretchY: number
    // textAlign: 'centre' | 'left' | 'right'
    // textColour: string
    // textFont: string
    textHeight: 35,
    // textVAlign: 'top' | 'bottom' | 'middle'
    tooltip: "native", // null | 'div'
    // tooltipClass: string
    tooltipDelay: 0,
    // txtOpt: boolean
    // txtScale: number
    // weight: boolean
    // weightFrom: any
    // weightGradient: any
    // weightMode: 'size' | 'colour' | 'both' | 'bgcolour' | 'bgoutline' | 'outline'
    // weightSize: number
    // weightSizeMax: number | null
    // weightSizeMin: number | null
    wheelZoom: false
    // zoom: number
    // zoomMax: number
    // zoomMin: number
    // zoomStep: number
  }

  return (
    <Cloud
      containerProps={containerProps}
      canvasProps={canvasProps}
      options={options}
    >
      <a key={1} style={{ color: "#f90042" }}>
        Attempted Information Leak
      </a>
      <a key={2} style={{ color: "#f90042" }}>
        Potentially Bad Traffic
      </a>
      <a key={3} style={{ color: "#f90042" }}>
        Information Leak
      </a>
      <a key={4} style={{ color: "#f90042" }}>
        Web Application Attack
      </a>
      <a key={5} style={{ color: "#f90042" }}>
        Detection of a Network Scan
      </a>
      <a key={6} style={{ color: "#f90042" }}>
        Potential Corporate Privacy Violation
      </a>
      <a key={7} style={{ color: "#f90042" }}>
        Trojan
      </a>
      <a key={8} style={{ color: "#f90042" }}>
        Worms
      </a>
      <a key={9} style={{ color: "#f90042" }}>
        Adware
      </a>
      <a key={10} style={{ color: "#f90042" }}>
        Mobile Malware
      </a>
      <a key={11} style={{ color: "#f90042" }}>
        Rootkits
      </a>
      <a key={12} style={{ color: "#f90042" }}>
        Wiper Malware
      </a>
      <a key={13} style={{ color: "#f90042" }}>
        Ransomware
      </a>
      <a key={14} style={{ color: "#f90042" }}>
        Fileless Malware
      </a>
      <a key={15} style={{ color: "#f90042" }}>
        Spyware
      </a>
      <a key={16} style={{ color: "#f90042" }}>
        Denial of Service Attack
      </a>
      <a key={17} style={{ color: "#f90042" }}>
        Attempted User Privilege Gain
      </a>
      <a key={18} style={{ color: "#f90042" }}>
        Social Engineering Attempted
      </a>
    </Cloud>
  )
}

export default App