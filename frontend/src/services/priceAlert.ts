import api from './api';

const priceAlertService = {
  async getPriceAlerts() {
    const response = await api.get('/api/v1/price-alerts');
    return response.data;
  },

  async createPriceAlert(productId: number, targetPrice: number) {
    const response = await api.post('/api/v1/price-alerts', {
      product_id: productId,
      target_price: targetPrice
    });
    return response.data;
  },

  async deletePriceAlert(alertId: number) {
    const response = await api.delete(`/api/v1/price-alerts/${alertId}`);
    return response.data;
  },

  async getProductPriceAlert(productId: number) {
    try {
      const response = await api.get(`/api/v1/price-alerts/product/${productId}`);
      return response.data;
    } catch (error) {
      return null;
    }
  }
};

export default priceAlertService; 