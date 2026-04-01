<template>
  <v-container fluid class="fill-height" style="background: linear-gradient(to right, #2196F3, #4CAF50);">
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card elevation="12" class="pa-6">
          <v-card-title class="text-h4 font-weight-bold text-center mb-4">
            Log In
          </v-card-title>
          <v-form @submit.prevent="login">
            <v-text-field
              v-model="username"
              label="Username"
              prepend-icon="mdi-account"
              required
            ></v-text-field>
            <v-text-field
              v-model="password"
              label="Password"
              prepend-icon="mdi-lock"
              type="password"
              required
            ></v-text-field>
            <v-btn
              type="submit"
              color="primary"
              block
              x-large
              class="mt-4"
            >
              Log In
            </v-btn>
          </v-form>
          <v-alert v-if="error" type="error" class="mt-4">{{ error }}</v-alert>
          <v-card-text class="text-center mt-4">
            Don't have an account? 
            <v-btn text color="primary" to="/signup">Sign Up</v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  name: 'LoginPage',
  data() {
    return {
      username: '',
      password: '',
      error: null
    }
  },
  methods: {
    ...mapActions('auth', ['loginUser']),
    async login() {
      try {
        this.error = null;
        await this.loginUser({ username: this.username, password: this.password });
        this.$router.push('/dashboard');
      } catch (error) {
        console.error('Login failed:', error);
        this.error = error.response?.data?.non_field_errors?.[0] || 'Login failed. Please try again.';
      }
    }
  }
}
</script>