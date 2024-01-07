// ================================================================================================
//  File Name: index.js
//  Description: Details of the Trace ( Incidents ( Bruteforce UserName )).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import React, { Fragment, useEffect, useRef } from 'react'
import Highcharts from 'highcharts'
import HighchartsWordcloud from 'highcharts/modules/wordcloud'
import { Card, CardBody, CardHeader, CardTitle } from 'reactstrap'

// Initialize the wordcloud module
HighchartsWordcloud(Highcharts)

const WordCloudChart = () => {
  const containerRef = useRef(null)

  useEffect(() => {
    const text =
      `Chapter 1. Down the Rabbit-Hole 
      Alice was beginning to get very tired of sitting by her sister on the bank, and of having nothing to do:
      once or twice she had peeped into the book her sister was reading, but it had no pictures or conversations
      in it, and what is the use of a book, thought Alice without pictures or conversation?
      So she was considering in her own mind (as well as she could, for the hot day made her feel very sleepy
      and stupid), whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking
      the daisies, when suddenly a White Rabbit with pink eyes ran close by her.`

    const lines = text.replace(/[():'?0-9]+/g, '').split(/[,\. ]+/g)
    const data = lines.reduce((arr, word) => {
      let obj = arr.find((obj) => obj.name === word)
      if (obj) {
        obj.weight += 1
      } else {
        obj = {
          name: word,
          weight: 1
        }
        arr.push(obj)
      }
      return arr
    }, [])

    const chartOptions = {
      accessibility: {},
      series: [
        {
          type: 'wordcloud',
          data,
          name: 'Occurrences'
        }
      ],
      title: {
        text: "", // Change the title text here
        align: 'left'
      },
      chart: {
        backgroundColor: 'transparent'
      },
      credits: {
        enabled: false
      }
      // subtitle: {
      //   text: 'An excerpt from chapter 1: Down the Rabbit-Hole', // Change the subtitle text here
      //   align: 'left'
      // }
      //   tooltip: {
      //     headerFormat: '<span style="font-size: 16px"><b>{point.key}</b></span><br>'
      //   }
    }


    // Create the Highcharts chart
    Highcharts.chart(containerRef.current, chartOptions)
  }, [])

  return (
    <Fragment>
      <Card>
        <CardHeader>
          <CardTitle>wordcloud2</CardTitle>
        </CardHeader>
        <CardBody>
          <div ref={containerRef} />
        </CardBody>
      </Card>
    </Fragment>
  )
}

export default WordCloudChart
