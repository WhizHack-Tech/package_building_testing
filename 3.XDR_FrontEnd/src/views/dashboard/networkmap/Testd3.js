// import React from 'react'
// import { Graph } from 'react-d3-graph'
// import { CardBody, Card } from "reactstrap"

// const Sample = () => {
//     const [ref, setRef] = React.useState(null)
//     const config = {
//         automaticRearrangeAfterDropNode: true,
//         collapsible: true,
//         directed: true,  
//         focusAnimationDuration: 0.75,
//         focusZoom: 1,
//         freezeAllDragEvents: true,
//         height: 800,
//         highlightDegree: 10,
//         highlightOpacity: 0.2,
//         linkHighlightBehavior: true,
//         maxZoom: 12,
//         minZoom: 0.05,
//         nodeHighlightBehavior: true,
//         panAndZoom: false,
//         staticGraph: false,
//         staticGraphWithDragAndDrop: false,
//         width: window.innerWidth,
//         d3: {
//           alphaTarget: 0.05,
//           gravity: -250,
//           linkLength: 120,
//           linkStrength: 2,
//           disableLinkForce: false
//         },
//         node: {
//             color: '#d3d3d3',
//             fontColor: 'black',
//             fontSize: 10,
//             fontWeight: 'normal',
//             highlightColor: 'red',
//             highlightFontSize: 14,
//             highlightFontWeight: 'bold',
//             highlightStrokeColor: 'red',
//             highlightStrokeWidth: 1.5,
//             // labelProperty: (n) => (n.name ? `${n.id} - ${n.name}` : n.id),
//             mouseCursor: 'pointer',
//             opacity: 0.9,
//             renderLabel: true,
//             size: 200,
//             strokeColor: 'none',
//             strokeWidth: 1.5,
//             svg: '',
//             symbolType: 'diamond'
//         },
//         link: {
//             color: "lightgray",
//             fontColor: "black",
//             fontSize: 8,
//             fontWeight: "normal",
//             highlightColor: "red",
//             highlightFontSize: 6,
//             highlightFontWeight: "normal",
//             labelProperty: "label",
//             mouseCursor: "pointer",
//             opacity: 1,
//             renderLabel: false,
//             semanticStrokeWidth: true,
//             strokeWidth: 3,
//             markerHeight: 4,
//             markerWidth: 6,
//             strokeDasharray: 0,
//             strokeDashoffset: 0,
//             strokeLinecap: "butt"
//         }
//     }
//     const data = {
//         links: [
//             // Groups
//             {
//                 source: 'Marvel',
//                 target: 'Heroes'
//             },
//             {
//                 source: 'Marvel',
//                 target: 'Villains'
//             },
//             {
//                 source: 'Marvel',
//                 target: 'Teams'
//             },
//             // Heroes
//             {
//                 source: 'Heroes',
//                 target: 'Spider-Man'
//             },
//             {
//                 source: 'Heroes',
//                 target: 'CAPTAIN MARVEL'
//             },
//             {
//                 source: 'Heroes',
//                 target: 'HULK'
//             },
//             {
//                 source: 'Heroes',
//                 target: 'Black Widow'
//             },
//             {
//                 source: 'Heroes',
//                 target: 'Daredevil'
//             },
//             {
//                 source: 'Heroes',
//                 target: 'Wolverine'
//             },
//             {
//                 source: 'Heroes',
//                 target: 'Captain America'
//             },
//             {
//                 source: 'Heroes',
//                 target: 'Iron Man'
//             },
//             {
//                 source: 'Heroes',
//                 target: 'THOR'
//             },
//             // Villains
//             {
//                 source: 'Villains',
//                 target: 'Dr. Doom'
//             },
//             {
//                 source: 'Villains',
//                 target: 'Mystique'
//             },
//             {
//                 source: 'Villains',
//                 target: 'Red Skull'
//             },
//             {
//                 source: 'Villains',
//                 target: 'Ronan'
//             },
//             {
//                 source: 'Villains',
//                 target: 'Magneto'
//             },
//             {
//                 source: 'Villains',
//                 target: 'Thanos'
//             },
//             {
//                 source: 'Villains',
//                 target: 'Black Cat'
//             },
//             // Teams
//             {
//                 source: 'Teams',
//                 target: 'Avengers'
//             },
//             {
//                 source: 'Teams',
//                 target: 'Guardians of the Galaxy'
//             },
//             {
//                 source: 'Teams',
//                 target: 'Defenders'
//             },
//             {
//                 source: 'Teams',
//                 target: 'X-Men'
//             },
//             {
//                 source: 'Teams',
//                 target: 'Fantastic Four'
//             },
//             {
//                 source: 'Teams',
//                 target: 'Inhumans'
//             }
//         ],
//         nodes: [
//             // Groups
//             {
//                 id: 'Marvel',
//                 symbolType: 'circle',
//                 color: 'black',
//                 size: 500,
//                 svg:'http://marvel-force-chart.surge.sh/marvel_force_chart_img/top_spiderman.png',
//                 fontSize: 25
//             },
//             {
//                 id: 'Heroes',
//                 symbolType: 'circle',
//                 color: 'red',
//                 size: 100
//             },
//             {
//                 id: 'Villains',
//                 symbolType: 'circle',
//                 color: 'red',
//                 size: 100
//             },
//             {
//                 id: 'Teams',
//                 symbolType: 'circle',
//                 color: 'red',
//                 size: 100
//             },
//             // Heroes
//             {
//                 id: 'Spider-Man',
//                 name: 'Peter Benjamin Parker',
//                 symbolType: 'circle',
//                 color: 'green',
//                 size: 120
//             },
//             {
//                 id: 'CAPTAIN MARVEL',
//                 name: 'Carol Danvers',
//                 symbolType: 'circle',
//                 color: 'green',
//                 size: 120
//             },
//             {
//                 id: 'HULK',
//                 name: 'Robert Bruce Banner',
//                 symbolType: 'circle',
//                 color: 'green',
//                 size: 120
//             },
//             {
//                 id: 'Black Widow',
//                 name: 'Natasha Alianovna Romanova',
//                 symbolType: 'circle',
//                 color: 'green',
//                 size: 120
//             },
//             {
//                 id: 'Daredevil',
//                 name: 'Matthew Michael Murdock',
//                 symbolType: 'circle',
//                 color: 'green',
//                 size: 120
//             },
//             {
//                 id: 'Wolverine',
//                 name: 'James Howlett',
//                 symbolType: 'circle',
//                 color: 'green',
//                 size: 120
//             },
//             {
//                 id: 'Captain America',
//                 name: 'Steven Rogers',
//                 symbolType: 'circle',
//                 color: 'green',
//                 size: 120
//             },
//             {
//                 id: 'Iron Man',
//                 name: 'Toasdasdasdasdny Stark',
//                 symbolType: 'circle',
//                 color: 'green',
//                 size: 120
//             },
//             {
//                 id: 'THOR',
//                 name: 'Thor Odinson',
//                 symbolType: 'circle',
//                 color: 'green',
//                 size: 120
//             },
//             // Villains
//             {
//                 id: 'Dr. Doom',
//                 name: 'Victor von Doom',
//                 symbolType: 'circle',
//                 color: 'green',
//                 size: 120
//             },
//             {
//                 id: 'Mystique',
//                 name: 'Unrevealed',
//                 symbolType: 'circle',
//                 color: 'green',
//                 size: 120
//             },
//             {
//                 id: 'Red Skull',
//                 name: 'Johann Shmidt',
//                 symbolType: 'circle',
//                 color: 'green',
//                 size: 120
//             },
//             {
//                 id: 'Ronan',
//                 name: 'Ronan',
//                 symbolType: 'circle',
//                 color: 'green',
//                 size: 120
//             },
//             {
//                 id: 'Magneto',
//                 name: 'Max Eisenhardt',
//                 symbolType: 'circle',
//                 color: 'green',
//                 size: 120
//             },
//             {
//                 id: 'Thanos',
//                 name: 'Thanos',
//                 symbolType: 'circle',
//                 color: 'green',
//                 size: 120
//             },
//             {
//                 id: 'Black Cat',
//                 name: 'Felicia Hardy',
//                 symbolType: 'circle',
//                 color: 'green',
//                 size: 120
//             },
//             // Teams
//             {
//                 id: 'Avengers',
//                 symbolType: 'circle',
//                 color: 'green',
//                 name: '',
//                 size: 120
//             },
//             {
//                 id: 'Guardians of the Galaxy',
//                 symbolType: 'circle',
//                 color: 'green',
//                 name: '',
//                 size: 120
//             },
//             {
//                 id: 'Defenders',
//                 symbolType: 'circle',
//                 color: 'green',
//                 name: '',
//                 size: 120
//             },
//             {
//                 id: 'X-Men',
//                 symbolType: 'circle',
//                 color: 'green',
//                 name: '',
//                 size: 120
//             },
//             {
//                 id: 'Fantastic Four',
//                 symbolType: 'circle',
//                 color: 'green',
//                 name: '',
//                 size: 120
//             },
//             {
//                 id: 'Inhumans',
//                 symbolType: 'circle',
//                 color: 'green',
//                 name: '',
//                 size: 120
//             }
//         ]
//     }
//     const onClickNode = function (nodeId) {
//       //window.alert(`Clicked node ${nodeId}`);
//     }

//     const onClickLink = function (source, target) {
//      //window.alert(`Clicked link between ${source} and ${target}`);
//     }


//     const resetNodesPositions = React.useCallback(() => {
//         if (ref) ref.resetNodesPositions()
//     }, [ref])

//     const handleRefChange = React.useCallback((ref) => {
//      setRef(ref)
//     }, [])

//     return (
//         <Card>
//             <CardBody>
//             {/* <button onClick={resetNodesPositions}>Reset Nodes</button> */}
//                 <Graph
//                     id="test"
//                     className="graph"
//                     data={data}
//                     config={config}
//                     onClickNode={onClickNode}
//                     onClickLink={onClickLink}
//                     // ref={handleRefChange}
//                 />
//             </CardBody>
//         </Card>
//     )
// }

// export default Sample
import React from 'react'
import { Graph } from 'react-d3-graph'
import { CardBody, Card } from "reactstrap"

const Sample = () => {
    const [ref, setRef] = React.useState(null)
    const config = {
        directed: true,
        automaticRearrangeAfterDropNode: true,
        collapsible: true,
        height: window.innerHeight,
        highlightDegree: 2,
        highlightOpacity: 0.2,
        linkHighlightBehavior: true,
        maxZoom: 12,
        minZoom: 0.05,
        nodeHighlightBehavior: true, // comment this to reset nodes positions to work
        panAndZoom: false,
        staticGraph: false,
        width: window.innerWidth,
        d3: {
            alphaTarget: 0.05,
            gravity: -250,
            linkLength: 120,
            linkStrength: 2
        },
        node: {
            color: '#000000',
            fontColor: 'red',
            fontSize: 10,
            fontWeight: 'normal',
            highlightColor: 'black',
            highlightFontSize: 14,
            highlightFontWeight: 'bold',
            highlightStrokeColor: 'black',
            highlightStrokeWidth: 1.5,
            labelProperty: (n) => (n.name ? `${n.id} - ${n.name}` : n.id),
            mouseCursor: 'crosshair',
            opacity: 0.9,
            renderLabel: true,
            size: 200,
            strokeColor: 'none',
            strokeWidth: 1.5,
            svg: '',
            symbolType: 'circle',
            viewGenerator: null
        },
        link: {
            color: '#766af8',
            highlightColor: 'green',
            mouseCursor: 'pointer',
            opacity: 1,
            semanticStrokeWidth: true,
            strokeWidth: 1,
            type: 'STRAIGHT'
        }
    }
    const data = {
        links: [
            // Groups
            {
                source: 'Marvel',
                target: 'Heroes'
            },
            {
                source: 'Marvel',
                target: 'Villains'
            },
            {
                source: 'Marvel',
                target: 'Teams'
            },
            // Heroes
            {
                source: 'Heroes',
                target: 'Spider-Man'
            },
            {
                source: 'Heroes',
                target: 'CAPTAIN MARVEL'
            },
            {
                source: 'Heroes',
                target: 'HULK'
            },
            {
                source: 'Heroes',
                target: 'Black Widow'
            },
            {
                source: 'Heroes',
                target: 'Daredevil'
            },
            {
                source: 'Heroes',
                target: 'Wolverine'
            },
            {
                source: 'Heroes',
                target: 'Captain America'
            },
            {
                source: 'Heroes',
                target: 'Iron Man'
            },
            {
                source: 'Heroes',
                target: 'THOR'
            },
            // Villains
            {
                source: 'Villains',
                target: 'Dr. Doom'
            },
            {
                source: 'Villains',
                target: 'Mystique'
            },
            {
                source: 'Villains',
                target: 'Red Skull'
            },
            {
                source: 'Villains',
                target: 'Ronan'
            },
            {
                source: 'Villains',
                target: 'Magneto'
            },
            {
                source: 'Villains',
                target: 'Thanos'
            },
            {
                source: 'Villains',
                target: 'Black Cat'
            },
            // Teams
            {
                source: 'Teams',
                target: 'Avengers'
            },
            {
                source: 'Teams',
                target: 'Guardians of the Galaxy'
            },
            {
                source: 'Teams',
                target: 'Defenders'
            },
            {
                source: 'Teams',
                target: 'X-Men'
            },
            {
                source: 'Teams',
                target: 'Fantastic Four'
            },
            {
                source: 'Teams',
                target: 'Inhumans'
            }
        ],
        nodes: [
            // Groups
            {
                id: 'Marvel',
                size: 100,
                symbolType: 'circle',
                color: 'green',
                fontSize: 10
            },
            {
                id: 'Heroes',
                symbolType: 'circle',
                color: 'blue',
                size: 100
            },
            {
                id: 'Villains',
                symbolType: 'circle',
                color: 'blue',
                size: 100
            },
            {
                id: 'Teams',
                symbolType: 'circle',
                color: 'red',
                size: 100
            },
            // Heroes
            {
                id: 'Spider-Man',
                name: 'Peter Benjamin Parker',
                symbolType: 'circle',
                color: 'red',
                size: 100
            },
            {
                id: 'CAPTAIN MARVEL',
                name: 'Carol Danvers',
                symbolType: 'circle',
                fontSize: 10,
                color: 'red',
                size: 100
            },
            {
                id: 'HULK',
                name: 'Robert Bruce Banner',
                size: 100,
                symbolType: 'circle',
                color: 'red'
            },
            {
                id: 'Black Widow',
                name: 'Natasha Alianovna Romanova',
                size: 100,
                symbolType: 'circle',
                color: 'red'
            },
            {
                id: 'Daredevil',
                name: 'Matthew Michael Murdock',
                size: 100,
                symbolType: 'circle',
                color: 'red'
            },
            {
                id: 'Wolverine',
                name: 'James Howlett',
                size: 100,
                symbolType: 'circle',
                color: 'red'
            },
            {
                id: 'Captain America',
                name: 'Steven Rogers',
                size: 100,
                symbolType: 'circle',
                color: 'red'
            },
            {
                id: 'Iron Man',
                name: 'Tony Stark',
                size: 100,
                symbolType: 'circle',
                color: 'red'
            },
            {
                id: 'THOR',
                name: 'Thor Odinson',
                size: 100,
                symbolType: 'circle',
                color: 'red'
            },
            // Villains
            {
                id: 'Dr. Doom',
                name: 'Victor von Doom',
                size: 100,
                symbolType: 'circle',
                color: 'red'
            },
            {
                id: 'Mystique',
                name: 'Unrevealed',
                size: 100,
                symbolType: 'circle',
                color: 'red'
            },
            {
                id: 'Red Skull',
                name: 'Johann Shmidt',
                size: 100,
                symbolType: 'circle',
                color: 'red'
            },
            {
                id: 'Ronan',
                name: 'Ronan',
                size: 100,
                symbolType: 'circle',
                color: 'red'
            },
            {
                id: 'Magneto',
                name: 'Max Eisenhardt',
                size: 100,
                symbolType: 'circle',
                color: 'red'
            },
            {
                id: 'Thanos',
                name: 'Thanos',
                size: 100,
                symbolType: 'circle',
                color: 'red'
            },
            {
                id: 'Black Cat',
                name: 'Felicia Hardy',
                size: 100,
                symbolType: 'circle',
                color: 'red'
            },
            // Teams
            {
                id: 'Avengers',
                name: '',
                size: 100,
                symbolType: 'circle',
                color: 'red'
            },
            {
                id: 'Guardians of the Galaxy',
                name: '',
                size: 100,
                symbolType: 'circle',
                color: 'red'
            },
            {
                id: 'Defenders',
                name: '',
                size: 100,
                symbolType: 'circle',
                color: 'red'
            },
            {
                id: 'X-Men',
                name: '',
                size: 100,
                symbolType: 'circle',
                color: 'red'
            },
            {
                id: 'Fantastic Four',
                name: '',
                size: 100,
                symbolType: 'circle',
                color: 'red'
            },
            {
                id: 'Inhumans',
                name: '',
                size: 100,
                symbolType: 'circle',
                color: 'red'
            }
        ]
    }

    const resetNodesPositions = React.useCallback(() => {
        if (ref) ref.resetNodesPositions()
    }, [ref])

    //  
    return (
        <Card>
            <CardBody>
                <button onClick={resetNodesPositions}>Reset Nodes</button>
                <Graph
                    id="test"
                    data={data}
                    config={config}
                    // ref={handleRefChange}
                />
            </CardBody>
        </Card>
    )

}
export default Sample
