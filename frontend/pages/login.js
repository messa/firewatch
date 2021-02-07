import React from 'react'
import { useRouter } from 'next/router'
import useSWR from 'swr'
import Layout from '../components/Layout'
import CheckList from '../components/CheckList'
import { fetcher, swrOptions } from '../util/swr'

function LoginPage() {
  return (
    <Layout>
      <h1>Login</h1>
      <p><a href='/api/auth/google'>Login via Google</a></p>
    </Layout>
  )
}

export default LoginPage
