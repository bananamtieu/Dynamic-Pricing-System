import React, { useEffect, useState } from "react";
import { fetchPredictedPrices, fetchPriceHistory } from "../api";
import "./ProductList.css";
import { MdDevices } from "react-icons/md"; // Electronics
import { FiHeadphones } from "react-icons/fi"; // Accessories
import { FaTools } from "react-icons/fa"; // Gadgets
import { GiWatch } from "react-icons/gi"; // Wearables
import { BsDatabase } from "react-icons/bs"; // Storage
import { FaArrowUp, FaArrowDown } from "react-icons/fa";
import PriceTrendModal from "./PriceTrendModal"; // Import modal component

const ProductList = () => {
  const [products, setProducts] = useState([]);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    const loadProducts = async () => {
      const data = await fetchPredictedPrices();
      setProducts(data);
    };
    loadProducts();
  }, []);

  // ✅ Function to return category icon
  const getCategoryIcon = (category) => {
    switch (category) {
      case "Electronics":
        return <MdDevices className="icon" />;
      case "Accessories":
        return <FiHeadphones className="icon" />;
      case "Gadgets":
        return <FaTools className="icon" />;
      case "Wearables":
        return <GiWatch className="icon" />;
      case "Storage":
        return <BsDatabase className="icon" />;
      default:
        return null;
    }
  };

  // ✅ Function to get price trend arrow
  const getPriceTrend = (prevPrice, currentPrice) => {
    if (currentPrice > prevPrice) {
      return (
        <span className="price-up">
          ${currentPrice} <FaArrowUp className="trend-arrow" />
        </span>
      );
    } else if (currentPrice < prevPrice) {
      return (
        <span className="price-down">
          ${currentPrice} <FaArrowDown className="trend-arrow" />
        </span>
      );
    }
    
    // No price change: Keep neutral color
    return <span className="price-neutral">${currentPrice}</span>;
  };

  // ✅ Handle opening the modal
  const handleShowTrend = async (product) => {
    setSelectedProduct(product);
    setShowModal(true);
  };

  return (
    <div className="product-list-container">
      <div className="product-list-wrapper">
        <h2 className="product-list-title">📊 Predicted Prices</h2>

        <div className="table-container">
          <table className="product-table">
            <thead>
              <tr>
                <th>Product ID</th>
                <th>Name</th>
                <th>Category</th>
                <th>Predicted Price</th>
                <th>Trend</th>
              </tr>
            </thead>
            <tbody>
              {products.map((product) => (
                <tr key={product.id}>
                  <td>{product.id}</td>
                  <td>{product.name}</td>
                  <td>
                    <span className="category">
                      {getCategoryIcon(product.category)} {product.category}
                    </span>
                  </td>
                  <td>
                    {getPriceTrend(product.prev_price, product.price)}
                  </td>
                  <td>
                    <button className="trend-btn" onClick={() => handleShowTrend(product)}>
                      Show Past Price Trend
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* ✅ Price Trend Modal */}
      {showModal && <PriceTrendModal product={selectedProduct} onClose={() => setShowModal(false)} />}
    </div>
  );
};

export default ProductList;
