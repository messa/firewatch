import React from 'react'
import Layout from '../components/Layout'
import CheckList from '../components/CheckList'

function IndexPage() {
  return (
    <Layout>
      <h1>Firewatch</h1>
      <p>Hello World!</p>
      <CheckList />
    </Layout>
  )
}

export default IndexPage
