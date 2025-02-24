import React, { useEffect, useState } from "react";
import { fetchPriceHistory } from "../api";
import "./PriceTrendModal.css";
import { Line } from "react-chartjs-2";
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

const PriceTrendModal = ({ product, onClose }) => {
  const [priceHistory, setPriceHistory] = useState([]);

  useEffect(() => {
    const loadPriceHistory = async () => {
      if (product) {
        const history = await fetchPriceHistory(product.id);
        setPriceHistory(history);
      }
    };
    loadPriceHistory();
  }, [product]);

  if (!product) return null;

  // ✅ Prepare data for chart
  const chartData = {
    labels: priceHistory.map((entry) => entry.date),
    datasets: [
      {
        label: `${product.name} Price Trend`,
        data: priceHistory.map((entry) => entry.price),
        borderColor: "#4CAF50",
        backgroundColor: "rgba(76, 175, 80, 0.2)",
        fill: true,
      },
    ],
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h2 className="modal-title">📉 {product.name} Price Trend</h2>
        <Line data={chartData} />
        <button className="close-btn" onClick={onClose}>
          Close
        </button>
      </div>
    </div>
  );
};

export default PriceTrendModal;
