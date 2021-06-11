import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchGappers, selectAllGappers } from './gappersSlicer';


export default function GappersList () {
  const fetchGappersStatus = useSelector(state => state.gappers.status)
  const gappers = useSelector(selectAllGappers)


  const dispatch = useDispatch()
  useEffect(() => {
    if (fetchGappersStatus === 'idle') {
      dispatch(fetchGappers())
    }
  }, [fetchGappersStatus, dispatch])

console.log('gappers', gappers)

  const renderedGappers = gappers.map(gapper => (
    <tr>
      <td>{gapper.ticker}</td>
      <td>{gapper.industry}</td>
    </tr>
  ))

  return (
    <table>
        {renderedGappers}
    </table>
  )
}
