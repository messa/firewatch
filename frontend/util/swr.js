export async function fetcher(...args) {
  const res = await fetch(...args)
  return res.json()
}

export const swrOptions = {
  refreshInterval: 3 * 1000,
  compare: (a, b) => false, // let's rerender every time to update the "ago" values
}
