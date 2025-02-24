import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000/api"; // Adjust if needed

export const fetchPredictedPrices = async () => {
  try {
    const productIds = Array.from({ length: 10 }, (_, i) => i + 1);

    const responses = await Promise.all(
      productIds.map(async (id) => {
        // Fetch suggested price & product details in parallel
        const [priceRes, productRes, historyRes] = await Promise.all([
          axios.get(`${API_BASE_URL}/suggest-price/${id}/`),
          axios.get(`${API_BASE_URL}/products/${id}/`),
          axios.get(`${API_BASE_URL}/price-history/${id}/`),
        ]);

        // Extract previous price from the last price entry in history
        const priceHistory = historyRes.data;
        const prev_price = priceHistory.length > 0 
          ? parseFloat(priceHistory[priceHistory.length - 1].price).toFixed(2)
          : "N/A"; // If no history, set as "N/A"

        return {
          id: id,
          name: productRes.data.name,
          category: productRes.data.category,
          price: priceRes.data.suggested_price.toFixed(2), // Ensure 2 decimal places
          prev_price: prev_price, // Last recorded price
        };
      })
    );

    return responses;
  } catch (error) {
    console.error("Error fetching predicted prices:", error);
    return [];
  }
};

export const fetchPriceHistory = async (productId) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/price-history/${productId}/`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching price history for product ${productId}:`, error);
      return [];
    }
};