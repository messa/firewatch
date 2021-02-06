import React from 'react'
import useSWR from 'swr'
import Link from 'next/link'
import ShowDate from './ShowDate'
import { fetcher, swrOptions } from '../util/swr'

function getStatusEmoji(ok) {
  if (ok === true) return '✅';
  if (ok === false) return '❌';
  return '🟡';
}

function CheckResults({ checkId }) {
  const { data, error, isValidating } = useSWR(`/api/http-checks/${encodeURIComponent(checkId)}/last-results`, fetcher, swrOptions)
  return (
    <div>
      {error && <p style={{ color: 'red' }}>Failed to load</p>}
      {data && (
        <table style={{ minWidth: '80%' }} className={isValidating ? 'loading' : ''}>
          <thead>
            <tr style={{ borderBottom: '1px solid #333' }}>
              <th>Time</th>
              <th>Status</th>
              <th>Duration</th>
            </tr>
          </thead>
          {data.last_results.map((result, i) => (
            <tbody key={i} style={{ borderBottom: '1px solid #aaa' }}>
              <tr>
                <td>
                  <ShowDate date={result.time} />
                </td>
                <td>
                  {getStatusEmoji(result.status_ok)}
                </td>
                <td>
                  {`${result.total_duration.toFixed(3)}\xa0s`}
                </td>
              </tr>
            </tbody>
          ))}
        </table>
      )}
    </div>
  )
}

export default CheckResults
