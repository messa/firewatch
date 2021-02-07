import React from 'react'
import { useRouter } from 'next/router'
import useSWR from 'swr'
import Layout from '../components/Layout'
import CheckResults from '../components/CheckResults'
import { fetcher, swrOptions } from '../util/swr'

function CheckDetailPage() {
  const router = useRouter()
  const { checkId } = router.query
  if (!checkId) {
    return <Layout />
  }
  const { data, error } = useSWR(`/api/http-checks/${encodeURIComponent(checkId)}`, fetcher, swrOptions)
  return (
    <Layout>
      <h1>HTTP Check</h1>
      {error && <p style={{ color: 'red' }}>Failed to load</p>}
      <p><b>Id:</b> <code>{checkId}</code></p>
      <p><b>URL:</b> <code>{data && data.http_check.url}</code></p>
      <p><b>Interval:</b> {data && data.http_check.interval} s</p>
      <h2>Last results</h2>
      <CheckResults checkId={checkId} />
    </Layout>
  )
}

export default CheckDetailPage
