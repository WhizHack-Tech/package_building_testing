// ================================================================================================
//  File Name: index.js
//  Description: Details of the Trace ( Incidents ( Bruteforce UserName )).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import React, { Fragment, useEffect, useRef, useState } from 'react'
import Highcharts from 'highcharts'
import HighchartsWordcloud from 'highcharts/modules/wordcloud'
import { Card, CardBody, CardHeader, CardTitle } from 'reactstrap'
import axios from '@axios'
import { useSelector } from 'react-redux'
import { token } from '@utils'
import DataNotFound from '../../dNotf'
import { useTranslation } from 'react-i18next'
import PreLoader from '../../preLoader'

// Initialize the wordcloud module
HighchartsWordcloud(Highcharts)


const WordCloudChart = () => {
  const { t } = useTranslation()
  const containerRef = useRef(null)
  const filterState = useSelector((store) => store.dashboard_chart)
  const [isLoading, setIsLoading] = useState(true)
  const [dataFound, setDataFound] = useState(false)
  const [checkApiData, setCheckApiData] = useState(true)


  useEffect(() => {
    setIsLoading(true)

    axios.get(`/incident-brut-username-trace?condition=${filterState.values ? filterState.values : 'last_1_hour'}`, { headers: { Authorization: token() } })
      .then((res) => {
        setIsLoading(false)

        if (res.data.message_type === "d_not_f") {
          setCheckApiData(false)
        }

        if (res.data.message_type === "success") {
          setDataFound(true)
          setCheckApiData(true)

          const data = res.data.data.reduce((arr, word) => {

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
                name: 'Total Count'
              }
            ],
            title: {
              text: '', // Change the title text here
              align: 'centre'
            },
            chart: {
              backgroundColor: 'transparent'
            },
            credits: {
              enabled: false
            }
          }

          Highcharts.chart(containerRef.current, chartOptions)

        }
      })
      .catch((error) => {
        setIsLoading(true)
        setDataFound(false) // Update state when data is not found
        console.error('Error fetching data:', error)
      })
  }, [filterState.values, filterState.refreshCount])

  return (
    <Fragment>
    <Card>
      <CardHeader>
        <CardTitle tag='h4'>{t('Bruteforce UserName')}</CardTitle>
      </CardHeader>
      <CardBody>
        {
          checkApiData ? (
            <div ref={containerRef} />
          ) : (
            <DataNotFound />
          )
        }
      </CardBody>
      {isLoading ? <PreLoader /> : null}
    </Card>
  </Fragment>
  )
}

export default WordCloudChart
