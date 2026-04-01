import { createStore } from 'vuex';
import auth from './modules/auth';

export default createStore({
   modules: {
        auth
   },
  state: {
    isAuthenticated: false,
    user: null,
    snackbar: {
      show: false,
      text: '',
      color: ''
    }
  },
  mutations: {
    SET_AUTHENTICATED(state, isAuthenticated) {
      state.isAuthenticated = isAuthenticated;
    },
    SET_USER(state, user) {
      state.user = user;
    },
    setUser(state, user) {
      state.user = user;
    },
    setSnackbar(state, payload) {
      state.snackbar.show = true;
      state.snackbar.text = payload.text;
      state.snackbar.color = payload.color;
    },
    closeSnackbar(state) {
      state.snackbar.show = false;
    }
  },
  actions: {
    login({ commit }, userData) {
      commit('SET_AUTHENTICATED', true);
      commit('SET_USER', userData);
    },
    logout({ commit }) {
      commit('SET_AUTHENTICATED', false);
      commit('SET_USER', null);
    },
    showSnackbar({ commit }, payload) {
      commit('setSnackbar', payload);
    }
  },
  getters: {
    isAuthenticated: state => state.isAuthenticated,
    user: state => state.user,
  },
})
