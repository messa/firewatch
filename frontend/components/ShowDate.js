import React from 'react'

function ShowDate({ date }) {
  if (!date) return null
  const dateObj = new Date(date)
  const diffMs = new Date().getTime() - dateObj.getTime()
  const diffStr = formatDifference(diffMs)
  return <span>{dateObj.toLocaleString()} ({diffStr} ago)</span>
}

function formatDifference(ms) {
  const s = Math.round(ms / 1000)
  return `${s} s`
}

export default ShowDate
