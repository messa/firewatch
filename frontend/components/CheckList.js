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

function CheckList({ projectId }) {
  const { data, error, isValidating } = useSWR(`/api/projects/${encodeURIComponent(projectId)}/checks`, fetcher, swrOptions)
  return (
    <div>
      {error && <p style={{ color: 'red' }}>Failed to load</p>}
      {data && (
        <table style={{ minWidth: '80%' }} className={isValidating ? 'loading' : ''}>
          <thead>
            <tr style={{ borderBottom: '1px solid #333' }}>
              <th>Id</th>
              <th>URL</th>
              <th colSpan={3}>Last result</th>
            </tr>
          </thead>
          {data.http_checks.map((check, i) => (
            <tbody key={i} style={{ borderBottom: '1px solid #aaa' }}>
              <tr>
                <td style={{ maxWidth: '4em', textOverflow: 'ellipsis' , overflow: 'hidden' }}>
                  <Link href={{ pathname: '/http-check', query: { checkId: check.check_id } }}>
                    <a>
                      <code>{check.check_id}</code>
                    </a>
                  </Link>
                </td>
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
            </tbody>
          ))}
        </table>
      )}
    </div>
  )
}

export default CheckList
