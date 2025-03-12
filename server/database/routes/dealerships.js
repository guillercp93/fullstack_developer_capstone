"use strict";

const express = require('express');
const router = express.Router();
const Dealerships = require('../schemas/dealership');

// Express route to fetch all dealerships
router.get('/fetchDealers', async (req, res) => {
  try {
    const documents = await Dealerships.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch Dealers by a particular state
router.get('/fetchDealers/:state', async (req, res) => {
  try {
    // Convert state parameter to lowercase for case-insensitive comparison
    const documents = await Dealerships.find({
      state: { $regex: new RegExp(req.params.state, "i") }
    });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch dealer by a particular id
router.get('/fetchDealer/:id', async (req, res) => {
  try {
    const document = await Dealerships.findOne({id: req.params.id});
    res.json(document);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

module.exports = router;
