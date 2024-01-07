import mock from '../mock'
import { paginateArray } from '../utils'

const data = [
  {
    responsive_id: '',
    id: 1,
    avatar: '10.jpg',
    username: "Korrie O'Crevy",
    full_name: "TATA",
    plan_descriptions: 'Frontend Developer ',
    email: 'kocrevy0@thetimes.co.uk',
    city: 'access to a potentially vulnerable web application',
    plan_creations_timestamp: '09/23/2016',
    salary: '$23896.35',
    age: '61',
    experience: '1 year',
    status: 2,
    ids: 23,
    ml: 45,
    dl:24,
    mlme: 'Potential Corporate Privacy Violation',
    dlme: 'Attempted Administrator Privilege Gain'
  },
  {
    responsive_id: '',
    id: 2,
    avatar: '',
    full_name: 'Glyn Giacoppo',
    username: "jAYDEEP",
    post: 'Software Test Engineer',
    email: 'ggiacoppo2r@apache.org',
    city: 'access to a potentially vulnerable web application',
    start_date: '04/15/2017',
    salary: '$24973.48',
    age: '41',
    experience: '7 Years',
    status: 2,
    ids: 24,
    ml: 45,
    dl:23,
    mlme: 'Potential Corporate Privacy Violation',
    dlme: 'Attempted Administrator Privilege Gain'
  },
  {
    responsive_id: '',
    id: 3,
    avatar: '',
    full_name: 'Glyn Giacoppo',
    username: "jAYDEEP",
    post: 'Software Test Engineer',
    email: 'ggiacoppo2r@apache.org',
    city: 'access to a potentially vulnerable web application',
    start_date: '04/15/2017',
    salary: '$24973.48',
    age: '41',
    experience: '7 Years',
    status: 2,
    ids: 44,
    ml: 45,
    dl:23,
    mlme: 'Potential Corporate Privacy Violation',
    dlme: 'Attempted Administrator Privilege Gain'
  },
  {
    responsive_id: '',
    id: 4,
    avatar: '',
    full_name: 'Glyn Giacoppo',
    username: "jAYDEEP",
    post: 'Software Test Engineer',
    email: 'ggiacoppo2r@apache.org',
    city: 'Butha-Buthe',
    start_date: '04/15/2017',
    salary: '$24973.48',
    age: '41',
    experience: '7 Years',
    status: 2,
    ids: 24,
    ml: 43,
    dl:23
  },
  {
    responsive_id: '',
    id: 5,
    avatar: '',
    full_name: 'Glyn Giacoppo',
    username: "jAYDEEP",
    post: 'Software Test Engineer',
    email: 'ggiacoppo2r@apache.org',
    city: 'Butha-Buthe',
    start_date: '04/15/2017',
    salary: '$24973.48',
    age: '41',
    experience: '7 Years',
    status: 2,
    ids: 44,
    ml: 45,
    dl:23
  },
  {
    responsive_id: '',
    id: 6,
    avatar: '',
    full_name: 'Glyn Giacoppo',
    username: "jAYDEEP",
    post: 'Software Test Engineer',
    email: 'ggiacoppo2r@apache.org',
    city: 'Butha-Buthe',
    start_date: '04/15/2017',
    salary: '$24973.48',
    age: '41',
    experience: '7 Years',
    status: 2,
    ids: 24,
    ml: 45,
    dl:24
  },
  {
    responsive_id: '',
    id: 7,
    avatar: '',
    full_name: 'Glyn Giacoppo',
    username: "jAYDEEP",
    post: 'Software Test Engineer',
    email: 'ggiacoppo2r@apache.org',
    city: 'Butha-Buthe',
    start_date: '04/15/2017',
    salary: '$24973.48',
    age: '41',
    experience: '7 Years',
    status: 2,
    ids: 24,
    ml: 45,
    dl:23
  },
  {
    responsive_id: '',
    id: 8,
    avatar: '',
    full_name: 'Glyn Giacoppo',
    username: "jAYDEEP",
    post: 'Software Test Engineer',
    email: 'ggiacoppo2r@apache.org',
    city: 'Butha-Buthe',
    start_date: '04/15/2017',
    salary: '$24973.48',
    age: '41',
    experience: '7 Years',
    status: 2,
    ids: 24,
    ml: 45,
    dl:24
  },
  {
    responsive_id: '',
    id: 10,
    avatar: '',
    full_name: 'Glyn Giacoppo',
    username: "jAYDEEP",
    post: 'Software Test Engineer',
    email: 'ggiacoppo2r@apache.org',
    city: 'Butha-Buthe',
    start_date: '04/15/2017',
    salary: '$24973.48',
    age: '41',
    experience: '7 Years',
    status: 2,
    ids: 24,
    ml: 43,
    dl:23
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