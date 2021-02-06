import React from 'react'

function ShowDate({ date }) {
  if (!date) return null
  const dateObj = new Date(date)
  const diffMs = new Date().getTime() - dateObj.getTime()
  const diffStr = formatDifference(diffMs)
  return <span>{dateObj.toLocaleString()} ({diffStr} ago)</span>
}

const floor = Math.floor

function formatDifference(ms) {
  const s = Math.round(ms / 1000)
  if (s < 60) return `${s} s`
  if (s < 3600) return `${floor(s / 60)} m ${s % 60} s`
  return `${floor(s / 3600)} h ${floor((s % 3600) / 60)} m ${s % 60} s`
}

export default ShowDate
