import React from 'react'
import Layout from '../components/Layout'
import CheckList from '../components/CheckList'

function IndexPage() {
  return (
    <Layout>
      <h2>HTTP Checks</h2>
      <CheckList />
    </Layout>
  )
}

export default IndexPage
