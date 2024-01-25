import React from "react";
import "./SearchField.css"
import { useState } from "react";
import axios from "../../../Constants/axios";

function SearchField() {
  const [query, setQuery] = useState("");

  const handleQuery = (e) => {
    setQuery(e.target.value);
    console.log(query);
  };

  const handleSearch = (e) => {
    e.preventDefault();
    axios
      .get(`shop/search-query?query=${query}`)
      .then((response) => {
        console.log(response.data);
      })
      .catch((e) => {
        if (e.response.status == 404) {
          console.log("No data");
        }
      });
  };
  return (
    <>
      <form action="" className="search-field">
        <input
          type="text"
          className="inp-field"
          placeholder="search products"
          onChange={handleQuery}
        />
        <button className="search-btn" type="submit" onClick={handleSearch}>
          Search
        </button>
      </form>
    </>
  );
}

export default SearchField;
