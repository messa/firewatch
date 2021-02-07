import React from 'react'
import Link from 'next/link'
import useSWR from 'swr'
import { fetcher, swrOptions } from '../util/swr'

function ProjectList() {
  const { data, error, isValidating } = useSWR('/api/projects', fetcher, swrOptions)
  return (
    <div>
      {error && <p style={{ color: 'red' }}>Failed to load</p>}
      {data && !data.projects.length && (
        <p>No projects to show.</p>
      )}
      {data && !!data.projects.length && (
        <ul className='big'>
          {data.projects.map(project => (
            <li key={project.project_id}>
              <Link href={{ pathname: '/project', query: { projectId: project.project_id } }}><a>
                <strong>{project.title}</strong>
              </a></Link>
            </li>
          ))}
        </ul>
      )}
      {data && !data.logged_in && (
        <p>You are not logged in – perhaps more projects would show if you <Link href='/login'><a>sign in</a></Link>.</p>
      )}
    </div>
  )
}

export default ProjectList
