module.exports.MedianPriceCalculator = async (event) => {
    let region = event.region;
    let medianPrice;

    // Define median prices for US, CA and BR
    const medianPrices = {
        US: 320000.0,
        CA: 240000.0,
        BR: 260000.0,
    };

    // Check if the input region is valid and retrieve the corresponding median price
    if (medianPrices.hasOwnProperty(region)) {
        medianPrice = medianPrices[region];
    } else {
        medianPrice = medianPrices.US; // default to US median price if region is unknown
        region = 'UNKNOWN REGION';
    }

    // Construct the response object
    const response = {
        statusCode: 200,
        body: JSON.stringify({region: region, medianPrice: medianPrice}),
        headers: {
            'X-Powered-By': 'AWS API Gateway & Lambda'
        },
        isBase64Encoded: false
    };

    return response;
};