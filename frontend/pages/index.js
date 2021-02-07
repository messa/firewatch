import React from 'react'
import Layout from '../components/Layout'

function IndexPage() {
  return (
    <Layout>
      <p>
        Please go to <a href='/login'>Login</a> or <a href='/dashboard'>Dashboard</a>.
      </p>
      <p>
        This page would not be used in production – there would be automatic redirect instead.
      </p>
    </Layout>
  )
}

export default IndexPage
