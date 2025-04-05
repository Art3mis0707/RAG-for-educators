const express = require('express');
const router = express.Router();
const { runRagQuery } = require('../controllers/ragController');

router.post('/', runRagQuery);

module.exports = router;
    