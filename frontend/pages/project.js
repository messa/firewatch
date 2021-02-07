import React from 'react'
import { useRouter } from 'next/router'
import useSWR from 'swr'
import Layout from '../components/Layout'
import CheckList from '../components/CheckList'
import { fetcher, swrOptions } from '../util/swr'

function ProjectPage() {
  const router = useRouter()
  const { projectId } = router.query
  if (!projectId) {
    return <Layout />
  }
  const { data, error } = useSWR(`/api/projects/${encodeURIComponent(projectId)}`, fetcher, swrOptions)
  return (
    <Layout>
      {error && <p style={{ color: 'red' }}>Failed to load</p>}
      {data && (
        <div>
          <h1>{data.project.title}</h1>
          <h2>HTTP Checks</h2>
          <CheckList projectId={projectId} />
        </div>
      )}
    </Layout>
  )
}

export default ProjectPage
