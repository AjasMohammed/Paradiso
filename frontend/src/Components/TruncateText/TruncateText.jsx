import React from 'react'

function TruncateText(props) {
    const {text, max_length} = props
  return (
    <>
        {text.length > max_length ? `${text.slice(0, max_length)}...` : text}
    </>
  )
}

export default TruncateText