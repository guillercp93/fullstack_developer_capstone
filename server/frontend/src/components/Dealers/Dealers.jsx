import React, { useState, useEffect } from 'react';
import "./Dealers.css";
import "../assets/style.css";
import Header from '../Header/Header';
import review_icon from "../assets/reviewicon.png"

const Dealers = () => {
  const [dealersList, setDealersList] = useState([]);
  // let [state, setState] = useState("")
  let [states, setStates] = useState([])

  // let root_url = window.location.origin
  const dealer_url = "/djangoapp/get_dealers";
  let dealer_url_by_state = "/djangoapp/get_dealers/";

  const filterDealers = async (state) => {
    dealer_url_by_state = dealer_url_by_state + state;
    const res = await fetch(dealer_url_by_state, {
      method: "GET"
    });
    const retobj = await res.json();
    if (retobj.status === 200) {
      let state_dealers = Array.from(retobj.dealers)
      setDealersList(state_dealers)
    }
  }

  const get_dealers = async () => {
    const res = await fetch(dealer_url, {
      method: "GET"
    });
    const retobj = await res.json();
    if (retobj.status === 200) {
      let all_dealers = Array.from(retobj.dealers)
      let states = [];
      all_dealers.forEach((dealer) => {
        states.push(dealer.state)
      });

      setStates(Array.from(new Set(states)))
      setDealersList(all_dealers)
    }
  }
  useEffect(() => {
    get_dealers();
  }, []);


  let isLoggedIn = sessionStorage.getItem("username") != null ? true : false;
  return (
    <>
      <Header home_page_items={<div></div>} />
      <div className="container mt-4">
        <div className="table-responsive" style={{ maxHeight: "90vh", overflow: "auto" }}>
          <table className="table table-striped table-bordered">
            <thead>
              <tr className="bg-light">
                <th scope="col" className="text-center align-middle">ID</th>
                <th scope="col" className="text-center align-middle">Dealer Name</th>
                <th scope="col" className="text-center align-middle">City</th>
                <th scope="col" className="text-center align-middle">Address</th>
                <th scope="col" className="text-center align-middle">Zip</th>
                <th scope="col" className="text-center align-middle">
                  <select className="form-select form-select-sm w-auto mx-auto"
                    name="state" id="state"
                    onChange={(e) => filterDealers(e.target.value)}
                  >
                    <option value="" selected disabled hidden>State</option>
                    <option value="All">All States</option>
                    {states.map(state => (
                      <option value={state}>{state}</option>
                    ))}
                  </select>
                </th>
                {isLoggedIn && <th scope="col" className="text-center align-middle">Review Dealer</th>}
              </tr>
            </thead>
            <tbody>
              {dealersList.map(dealer => (
                <tr>
                  <td className="text-center align-middle">{dealer.id}</td>
                  <td className="text-center align-middle"><a href={'/dealer/' + dealer['id']}>{dealer['full_name']}</a></td>
                  <td className="text-center align-middle">{dealer.city}</td>
                  <td className="text-center align-middle">{dealer.address}</td>
                  <td className="text-center align-middle">{dealer.zip}</td>
                  <td className="text-center align-middle">{dealer.state}</td>
                  {isLoggedIn && <td className="text-center align-middle"><a href={`/postreview/${dealer['id']}`}><img src={review_icon} className="review_icon" alt="Post Review" /></a></td>}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </>
  )
}

export default Dealers
