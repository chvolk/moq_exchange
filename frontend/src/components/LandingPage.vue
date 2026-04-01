<template>
  <v-container fluid class="pa-0">
    <v-row class="hero-section align-center justify-center" style="height: 100vh;">
      <v-col cols="12" md="8" class="text-center">
        <h1 class="text-h2 font-weight-bold mb-4">Welcome to Moq Exchange</h1>
        <p class="text-h5 mb-6">Buy low, sell high. Play the weekly challenge and climb the leaderboard.</p>
        <v-btn x-large color="primary" class="mr-4" to="/signup" v-if="!isAuthenticated">Get Started</v-btn>
        <v-btn x-large color="primary" class="mr-4" to="/dashboard" v-else>Go to Dashboard</v-btn>
        <v-btn x-large outlined to="/login" v-if="!isAuthenticated">Login</v-btn>
        <v-btn x-large outlined to ="/" v-else @click="signOut" >Logout</v-btn>
      </v-col>
    </v-row>

    <v-row class="features-section py-12">
      <v-col cols="12" md="4" v-for="feature in features" :key="feature.title">
        <v-card class="mx-auto" max-width="400">
          <v-card-title>{{ feature.title }}</v-card-title>
          <v-card-text>{{ feature.description }}</v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row class="cta-section py-12 align-center justify-center" style="background-color: #f5f5f5;">
      <v-col cols="12" md="8" class="text-center">
        <h2 class="text-h4 mb-4">Ready to start trading?</h2>
        <v-btn x-large color="success" to="/signup">Sign Up Now</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
  name: 'LandingPage',
  data: () => ({
    features: [
      { title: 'Risk-Free Trading', description: 'Practice trading with virtual money and learn the ins and outs of the stock market.' },
      { title: 'Compete with Friends', description: 'Create leagues, invite friends, and see who can build the best performing portfolio.' },
      { title: 'Real-Time Data', description: 'Get access to real-time stock data and market trends to inform your decisions.' },
    ],
  }),
  computed: {
    ...mapGetters('auth', ['isAuthenticated']),
  },
  methods: {
    ...mapActions('auth', ['logout']),
    async signOut() {
      await this.logout();
      this.$router.push('/');
    },
  },
}
</script>

<style scoped>
.hero-section {
  background: linear-gradient(to right, #4CAF50, #2196F3);
  color: white;
}
</style>