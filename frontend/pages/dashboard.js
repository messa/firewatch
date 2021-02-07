import React from 'react'
import Layout from '../components/Layout'
import ProjectList from '../components/ProjectList'

function DashboardPage() {
  return (
    <Layout>
      <h1>Projects</h1>
      <ProjectList />
    </Layout>
  )
}

export default DashboardPage
