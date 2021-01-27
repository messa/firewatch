import React from 'react'
import useSWR from 'swr'
import ShowDate from './ShowDate'

async function fetcher(...args) {
  const res = await fetch(...args)
  const data = res.json()
  return data
}

function getStatusEmoji(ok) {
  if (ok === true) return '✅';
  if (ok === false) return '❌';
  return '🟡';
}

const swrOptions = {
  refreshInterval: 3 * 1000,
  compare: (a, b) => false, // let's rerender every time to update the "ago" values
}

function CheckList() {
  const { data, error } = useSWR('/api/checks', fetcher, swrOptions)
  return (
    <div>
      <h2>HTTP Checks</h2>
      {error && <p>Failed to load</p>}
      {data && (
        <table style={{ minWidth: '80%' }}>
          <thead>
            <tr>
              <th>URL</th>
              <th colSpan={3}>Last result</th>
            </tr>
          </thead>
          <tbody>
            {data.http_checks.map((check, i) => (
              <tr key={i}>
                <td>
                  <code>{check.url}</code>
                </td>
                <td>
                  <ShowDate date={check.last_result && check.last_result.time} />
                </td>
                <td>
                  {getStatusEmoji(check.last_result && check.last_result.status_ok)}
                </td>
                <td>
                  {check.last_result && `${check.last_result.total_duration.toFixed(3)}\xa0s`}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}

export default CheckList
