import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import "./Dealers.css";
import "../assets/style.css";
import positive_icon from "../assets/positive.png"
import neutral_icon from "../assets/neutral.png"
import negative_icon from "../assets/negative.png"
import review_icon from "../assets/reviewbutton.png"
import Header from '../Header/Header';

const Dealer = () => {


  const [dealer, setDealer] = useState({});
  const [reviews, setReviews] = useState([]);
  const [unreviewed, setUnreviewed] = useState(false);
  const [postReview, setPostReview] = useState(<></>)

  let curr_url = window.location.href;
  let root_url = curr_url.substring(0, curr_url.indexOf("dealer"));
  let params = useParams();
  let id = params.id;
  let dealer_url = root_url + `djangoapp/get_dealer/${id}`;
  let reviews_url = root_url + `djangoapp/reviews/dealer/${id}`;
  let post_review = root_url + `postreview/${id}`;

  const get_dealer = async () => {
    const res = await fetch(dealer_url, {
      method: "GET"
    });
    const retobj = await res.json();

    if (retobj.status === 200) {
      setDealer(retobj.dealer)
    }
  }

  const get_reviews = async () => {
    const res = await fetch(reviews_url, {
      method: "GET"
    });
    const retobj = await res.json();

    if (retobj.status === 200) {
      if (retobj.reviews.length > 0) {
        setReviews(retobj.reviews)
      } else {
        setUnreviewed(true);
      }
    }
  }

  const senti_icon = (sentiment) => {
    let icon = sentiment === "positive" ? positive_icon : sentiment === "negative" ? negative_icon : neutral_icon;
    return icon;
  }

  useEffect(() => {
    get_dealer();
    get_reviews();
    if (sessionStorage.getItem("username")) {
      setPostReview(<a href={post_review}><img src={review_icon} style={{ width: '10%', marginLeft: '10px', marginTop: '10px' }} alt='Post Review' /></a>)


    }
  }, []);


  return (
    <>
      <Header />
      <div className="container-fluid">
        <h1 className="text-secondary">{dealer.full_name}{postReview}</h1>
        <h4 className="text-secondary">{dealer.city}, {dealer.address}, Zip - {dealer.zip}, {dealer.state}</h4>
      </div>
      <div className="reviews_panel">
        {reviews.length === 0 && unreviewed === false ? (
          <span className="text-muted">Loading Reviews....</span>
        ) : unreviewed === true ? <div className="alert alert-info">No reviews yet!</div> :
          reviews.map(review => (
            <div className="card shadow-sm review_panel" key={review.id}>
              <img src={senti_icon(review.sentiment)} className="emotion_icon position-absolute" alt='Sentiment' />
              <div className="review card-body">
                <p className="card-text">{review.review}</p>
                <div className="reviewer text-muted">{review.name} - {review.car_make} {review.car_model} {review.car_year}</div>
                <div className="review_date text-muted">
                  <small>{new Date(review.purchase_date).toLocaleDateString()}</small>
                </div>
              </div>
            </div>
          ))}
      </div>
    </>
  )
}

export default Dealer
