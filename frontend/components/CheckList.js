import React from 'react'
import useSWR from 'swr'

async function fetcher(...args) {
  const res = await fetch(...args)
  return res.json()
}

function CheckList() {
  const { data, error } = useSWR('/api/checks', fetcher)
  return (
    <div>
      <h2>HTTP Checks</h2>
      {data && data.http_checks.map(check => (
        <div>
          <p>URL: <code>{check.url}</code></p>
        </div>
      ))}
    </div>
  )
}

export default CheckList