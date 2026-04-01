import axios from 'axios';

const state = {
  token: localStorage.getItem('token') || null,
  user: null,
};

const getters = {
  isAuthenticated: state => !!state.token,
  user: state => state.user,
};

const actions = {
  async loginUser({ commit }, credentials) {
    try {
      const response = await axios.post('/api/login/', credentials);
      const token = response.data.token;
      localStorage.setItem('token', token);
      commit('setToken', token);
      return response;
    } catch (error) {
      console.error('Login error:', error);
      if (error.response && error.response.data) {
        throw new Error(error.response.data.non_field_errors?.[0] || 'Login failed');
      } else {
        throw new Error('Network error. Please try again.');
      }
    }
  },
  async logout({ commit }) {
    localStorage.removeItem('token');
    commit('SET_TOKEN', null);
    commit('SET_USER', null);
  },
};

const mutations = {
  SET_TOKEN(state, token) {
    state.token = token;
  },
  SET_USER(state, user) {
    state.user = user;
  },
  setToken(state, token) {
    state.token = token;
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};