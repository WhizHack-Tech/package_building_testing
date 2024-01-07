import mock from '../mock'

const data = {
  support_tracker: {
    title: 'Support Tracker',
    last_days: ['Last 28 Days', 'Last Month', 'Last Year'],
    totalTicket: 163,
    newTicket: 29,
    openTicket: 63,
    percentage: 80,
    responseTime: 1
  },
  avg_sessions: {
    agents: 272,
    last_days: ['Last 28 Days', 'Last Month', 'Last Year'],
    growth: '+5.2%',
    growth_days: ' last 10 days',
    AWS_Agents: 100,
    Azure_Agents: 1000,
    GCP_Agents: 902,
    OnPrim_Agents: 13
  },
  revenue_report: {
    years: ['2020', '2019', '2018'],
    price: '25,852',
    budget: '56,800'
  },
  sales_report: {
    // years: ['2020', '2019', '2018'],
    // price: '25,852',
    years: '2020',
    total_sale: 12000
  },
  goal_overview: {
    completed: '786,617',
    inProgress: '13,561'
  },
  revenue: {
    thisMonth: '86,589',
    lastMonth: '73,683'
  },
  product_orders: {
    last_days: ['Last 28 Days', 'Last Month', 'Last Year'],
    total: 123,
    chart_info: { Silver: 2, Gold: 9, Diamond: 1 }
  },
  sessions_device: {
    last_days: ['Last 28 Days', 'Last Month', 'Last Year'],
    chart_info: [
      {
        icon: 'Monitor',
        name: 'Windows OS',
        iconColor: 'text-primary',
        usage: 58.6,
        upDown: 2
      },
      {
        icon: 'Monitor',
        name: 'MacOS',
        iconColor: 'text-warning',
        usage: 34.9,
        upDown: 8
      },
      {
        icon: 'Monitor',
        name: 'Ubuntu',
        iconColor: 'text-danger',
        usage: 6.5,
        upDown: -5
      }
    ]
  },
  customers: {
    last_days: ['Last 28 Days', 'Last Month', 'Last Year'],
    listData: [
      {
        icon: 'Circle',
        iconColor: 'text-primary',
        text: 'New',
        result: 690
      },
      {
        icon: 'Circle',
        iconColor: 'text-warning',
        text: 'Returning',
        result: 258
      },
      {
        icon: 'Circle',
        iconColor: 'text-danger',
        text: 'Referrals',
        result: 149
      }
    ]
  }
}

mock.onGet('/card/card-analytics/support-tracker').reply(() => [200, data.support_tracker])
mock.onGet('/card/card-analytics/avg-sessions').reply(() => [200, data.avg_sessions])
mock.onGet('/card/card-analytics/revenue-report').reply(() => [200, data.revenue_report])
mock.onGet('/card/card-analytics/goal-overview').reply(() => [200, data.goal_overview])
mock.onGet('/card/card-analytics/sales').reply(() => [200, data.sales_report])
mock.onGet('/card/card-analytics/revenue').reply(() => [200, data.revenue])
mock.onGet('/card/card-analytics/product-orders').reply(() => [200, data.product_orders])
mock.onGet('/card/card-analytics/sessions-device').reply(() => [200, data.sessions_device])
mock.onGet('/card/card-analytics/customers').reply(() => [200, data.customers])
