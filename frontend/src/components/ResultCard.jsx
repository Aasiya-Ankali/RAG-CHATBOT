
import React from "react";

function ResultCard({ source }) {
  if (!source) {
    return null;
  }

  return (
    <div
      style={{
        border: "1px solid gray",
        borderRadius: "8px",
        padding: "15px",
        margin: "10px 0",
        display : "flex",
        boxShadow: "#161515",
      }}
    >
      <div>
        <div><strong>Product :{source.product_name}</strong></div>
        <div><strong>Reviews:</strong>{source.text}</div>  
        <div><strong>Category:</strong> {source.category }</div>
        <div><strong>Rating:</strong> {source.rating }</div>
      </div>
    </div>
  )
}

export default ResultCard;
