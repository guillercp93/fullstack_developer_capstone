import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import "../assets/style.css";
import Header from '../Header/Header';
import "./Dealers.css";


const PostReview = () => {
  const [dealer, setDealer] = useState({});
  const [review, setReview] = useState("");
  const [model, setModel] = useState();
  const [year, setYear] = useState("");
  const [date, setDate] = useState("");
  const [carmodels, setCarmodels] = useState([]);

  const curr_url = window.location.href;
  const root_url = curr_url.substring(0, curr_url.indexOf("postreview"));
  let { id } = useParams();
  const dealer_url = root_url + `djangoapp/get_dealer/${id}`;
  const review_url = root_url + `djangoapp/add_review`;
  const carmodels_url = root_url + `djangoapp/get_cars`;

  const postreview = async () => {
    let name = sessionStorage.getItem("firstname") + " " + sessionStorage.getItem("lastname");
    //If the first and second name are stores as null, use the username
    if (name.includes("null")) {
      name = sessionStorage.getItem("username");
    }
    if (!model || review === "" || date === "" || year === "" || model === "") {
      alert("All details are mandatory")
      return;
    }

    const model_split = model.split(" ");
    const make_chosen = model_split[0];
    const model_chosen = model_split[1];

    const jsoninput = JSON.stringify({
      "name": name,
      "dealership": id,
      "review": review,
      "purchase": true,
      "purchase_date": date,
      "car_make": make_chosen,
      "car_model": model_chosen,
      "car_year": year,
    });

    console.debug(jsoninput);
    const res = await fetch(review_url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: jsoninput,
    });

    const json = await res.json();
    if (json.status === 200) {
      window.location.href = window.location.origin + "/dealer/" + id;
    }

  }
  const get_dealer = async () => {
    const res = await fetch(dealer_url, {
      method: "GET"
    });
    const retobj = await res.json();
    if (retobj.status === 200) {
      setDealer(retobj.dealer)
    }
  }

  const get_cars = async () => {
    const res = await fetch(carmodels_url, {
      method: "GET"
    });
    const retobj = await res.json();

    let carmodelsarr = Array.from(retobj.CarModels)
    setCarmodels(carmodelsarr)
  }
  useEffect(() => {
    get_dealer();
    get_cars();
  }, []);


  return (
    <>
      <Header />
      <div className="container mt-4">
        <div className="row justify-content-center">
          <div className="col-md-8">
            <h1 className="text-primary mb-4">{dealer.full_name}</h1>
            <div className="mb-4 col-md-12">
              <label htmlFor="review" className="form-label">Your Review</label>
              <textarea
                className="form-control"
                id="review"
                rows="5"
                onChange={(e) => setReview(e.target.value)}
                placeholder="Write your review here..."
              ></textarea>
            </div>

            <div className="mb-3 col-md-12">
              <label htmlFor="cars" className="form-label">Car Make and Model</label>
              <select
                className="form-select"
                id="cars"
                onChange={(e) => setModel(e.target.value)}
              >
                <option value="" selected disabled hidden>Choose Car Make and Model</option>
                {carmodels.map(carmodel => (
                  <option key={carmodel.CarMake + carmodel.CarModel} value={carmodel.CarMake + " " + carmodel.CarModel}>
                    {carmodel.CarMake} {carmodel.CarModel}
                  </option>
                ))}
              </select>
            </div>

            <div className="row">
              <div className="mb-4 col-md-6">
                <label htmlFor="carYear" className="form-label">Car Year</label>
                <input
                  type="number"
                  className="form-control"
                  id="carYear"
                  onChange={(e) => setYear(e.target.value)}
                  max={2025}
                  min={2015}
                  placeholder="Enter year between 2015-2025"
                />
              </div>

              <div className="mb-3 col-md-6">
                <label htmlFor="purchaseDate" className="form-label">Purchase Date</label>
                <input
                  type="date"
                  className="form-control"
                  id="purchaseDate"
                  onChange={(e) => setDate(e.target.value)}
                />
              </div>
            </div>

            <div className="d-grid gap-2">
              <button className="btn btn-primary btn-lg" onClick={postreview}>
                Post Review
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}
export default PostReview
