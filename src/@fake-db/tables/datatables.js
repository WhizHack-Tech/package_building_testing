import mock from '../mock'
import { paginateArray } from '../utils'

const data = [
  {
    responsive_id: '',
    id: 1,
    avatar: '10.jpg',
    plan_name: "Korrie O'Crevy",
    full_name: "TATA",
    plan_descriptions: 'Frontend Developer ',
    email: 'kocrevy0@thetimes.co.uk',
    city: 'Krasnosilka',
    plan_creations_timestamp: '09/23/2016',
    salary: '$23896.35',
    age: '61',
    experience: '1 Year',
    status: 2
  },
  {
    responsive_id: '',
    id: 100,
    avatar: '',
    full_name: 'Glyn Giacoppo',
    full_name2: "jAYDEEP",
    post: 'Software Test Engineer',
    email: 'ggiacoppo2r@apache.org',
    city: 'Butha-Buthe',
    start_date: '04/15/2017',
    salary: '$24973.48',
    age: '41',
    experience: '7 Years',
    status: 2
  }
]

mock.onGet('/api/datatables/initial-data').reply(config => {
  return [200, data]
})

mock.onGet('/api/datatables/data').reply(config => {
  // eslint-disable-next-line object-curly-newline
  const { q = '', perPage = 10, page = 1 } = config
  /* eslint-enable */

  mock.onGet('/api/datatables/tables').reply(config => {
    const { id } = config
    const user = data.users.find(i => i.id === id)
    return [200, { user }]
  })

  const queryLowered = q.toLowerCase()
  const filteredData = data.filter(
    item =>
      /* eslint-disable operator-linebreak, implicit-arrow-linebreak */
      item.full_name.toLowerCase().includes(queryLowered) ||
      item.post.toLowerCase().includes(queryLowered) ||
      item.email.toLowerCase().includes(queryLowered) ||
      item.age.toLowerCase().includes(queryLowered) ||
      item.salary.toLowerCase().includes(queryLowered) ||
      item.start_date.toLowerCase().includes(queryLowered)
  )
  /* eslint-enable  */

  return [
    200,
    {
      allData: data,
      invoices: paginateArray(filteredData, perPage, page),
      total: filteredData.length
    }
  ]
})
