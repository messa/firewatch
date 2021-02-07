import React from 'react'
import { useRouter } from 'next/router'
import useSWR from 'swr'
import Layout from '../components/Layout'
import CheckList from '../components/CheckList'
import { fetcher, swrOptions } from '../util/swr'

function LoginPage() {
  const { data, error } = useSWR(`/api/auth/login-methods`, fetcher, swrOptions)
  return (
    <Layout>
      <h1>Login</h1>
      {error && <p style={{ color: 'red' }}>Failed to load</p>}
      {data && (
        <div>
          {data.login_methods.google && (
            <p><a href='/api/auth/google'>Sign in via Google</a></p>
          )}
          {data.login_methods.dev && (
            <p><a href='/api/auth/dev'>Development login</a></p>
          )}
        </div>
      )}
    </Layout>
  )
}

export default LoginPage
