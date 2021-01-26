import React from 'react'
import Head from 'next/head'
import Header from './Header'
import styles from './Layout.module.css'


function Layout({ children }) {
  return (
    <div className='Layout'>
      <Head>
        <title>Firewatch</title>
      </Head>
      <Header />
      <div className='container'>
        {children}
      </div>
    </div>
  )
}

export default Layout
