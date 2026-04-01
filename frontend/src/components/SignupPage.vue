<template>
  <v-container fluid class="fill-height" style="background: linear-gradient(to right, #4CAF50, #2196F3);">
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card elevation="12" class="pa-6">
          <v-card-title class="text-h4 font-weight-bold text-center mb-4">
            Join Moq Exchange
          </v-card-title>
          <v-form @submit.prevent="signup">
            <v-text-field
              v-model="username"
              label="Username"
              prepend-icon="mdi-account"
              required
            ></v-text-field>
            <v-text-field
              v-model="email"
              label="Email"
              prepend-icon="mdi-email"
              type="email"
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
              Sign Up
            </v-btn>
          </v-form>
          <v-alert v-if="error" type="error" class="mt-4">{{ error }}</v-alert>
          <v-card-text class="text-center mt-4">
            Already have an account? 
            <v-btn text color="primary" to="/login">Log In</v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { useRouter } from 'vue-router';
import authService from '@/services/auth';

export default {
  name: 'SignupPage',
  setup() {
    const router = useRouter();
    return { router };
  },
  data: () => ({
    username: '',
    email: '',
    password: '',
    error: null,
  }),
  methods: {
    async signup() {
      try {
        console.log('Attempting to signup with:', { username: this.username, email: this.email });
        const response = await authService.signup({
          username: this.username,
          email: this.email,
          password: this.password,
        });
        console.log('Signup successful', response);
        this.error = null;
        this.$emit('signup-success', 'Welcome aboard! Your account has been created successfully.');
        await new Promise(resolve => setTimeout(resolve, 1000));
        this.router.push('/');
      } catch (error) {
        console.error('Signup failed', error);
        authService.logAxiosError(error);
        this.error = error.response?.data?.message || 'An error occurred during signup. Please try again.';
      }
    },
  },
}
</script>