<template>
  <div class="landing-page">
    <!-- Hero -->
    <div class="hero-section">
      <!-- Floating bubbles -->
      <div class="bubbles" aria-hidden="true">
        <span v-for="n in 12" :key="n" class="bubble"></span>
      </div>

      <div class="hero-content">
        <p class="hero-tagline anim-fade-down">Fantasy Stock Trading</p>
        <h1 class="hero-title anim-fade-up">Trade Smarter. Compete Harder.</h1>
        <p class="hero-subtitle anim-fade-up anim-delay-1">Build your portfolio with real market data, climb the leaderboard, and earn MOQ in a risk-free stock market game.</p>
        <div class="d-flex justify-center ga-3 flex-wrap anim-fade-up anim-delay-2">
          <v-btn size="x-large" color="white" class="hero-cta-primary" to="/signup" v-if="!isAuthenticated">
            Get Started
            <v-icon end>mdi-arrow-right</v-icon>
          </v-btn>
          <v-btn size="x-large" color="white" class="hero-cta-primary" to="/dashboard" v-else>
            Go to Dashboard
            <v-icon end>mdi-arrow-right</v-icon>
          </v-btn>
          <v-btn size="x-large" variant="outlined" class="hero-cta-secondary" to="/login" v-if="!isAuthenticated">Login</v-btn>
          <v-btn size="x-large" variant="outlined" class="hero-cta-secondary" to="/" v-else @click="signOut">Logout</v-btn>
        </div>
      </div>

      <!-- Scroll indicator -->
      <div class="scroll-indicator anim-fade-up anim-delay-3">
        <v-icon color="rgba(255,255,255,0.5)" size="28" class="bounce-arrow">mdi-chevron-double-down</v-icon>
      </div>

      <!-- Wave transition -->
      <div class="hero-wave">
        <svg viewBox="0 0 1440 120" preserveAspectRatio="none">
          <path d="M0,60 C240,120 480,0 720,60 C960,120 1200,0 1440,60 L1440,120 L0,120 Z" fill="#ffffff"/>
        </svg>
      </div>
    </div>

    <!-- Features -->
    <section class="features-section">
      <div class="features-inner">
        <div class="text-center mb-6">
          <h2 class="text-h4 font-weight-bold section-title" ref="featuresTitle">How It Works</h2>
          <div class="section-divider"></div>
        </div>
        <div class="features-grid">
          <v-card
            v-for="(feature, i) in features"
            :key="feature.title"
            class="feature-card"
            elevation="2"
            :class="{ 'anim-visible': featuresVisible }"
            :style="{ animationDelay: (i * 0.15) + 's' }"
          >
            <v-card-text class="text-center pa-6">
              <div class="feature-icon-bg mb-4">
                <v-icon size="32" color="primary">{{ feature.icon }}</v-icon>
              </div>
              <h3 class="text-h6 font-weight-bold mb-2">{{ feature.title }}</h3>
              <p class="text-body-2" style="color: rgba(0,0,0,0.6); line-height: 1.6;">{{ feature.description }}</p>
            </v-card-text>
          </v-card>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="cta-section">
      <div class="cta-wave-top">
        <svg viewBox="0 0 1440 80" preserveAspectRatio="none">
          <path d="M0,40 C360,80 720,0 1080,40 C1260,60 1380,20 1440,40 L1440,0 L0,0 Z" fill="#ffffff"/>
        </svg>
      </div>
      <div class="cta-inner">
        <h2 class="text-h4 font-weight-bold mb-2" style="color: white;">Ready to start trading?</h2>
        <p class="text-body-1 mb-6" style="color: rgba(255,255,255,0.7);">Join the exchange and compete with players worldwide.</p>
        <v-btn size="x-large" color="white" class="cta-btn" to="/signup">
          Sign Up Now
          <v-icon end>mdi-arrow-right</v-icon>
        </v-btn>
      </div>
    </section>

    <!-- Footer -->
    <footer class="landing-footer">
      <span style="font-size: 0.8rem; color: rgba(0,0,0,0.4);">&copy; {{ new Date().getFullYear() }} North Atlantic Tech</span>
      <v-btn icon variant="text" size="small" href="https://discord.gg/8jkae3hKW5" target="_blank" rel="noopener noreferrer">
        <v-icon color="#5865F2">mdi-discord</v-icon>
      </v-btn>
    </footer>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
  name: 'LandingPage',
  data: () => ({
    featuresVisible: false,
    features: [
      { icon: 'mdi-shield-check', title: 'Risk-Free Trading', description: 'Practice trading with virtual money and learn the ins and outs of the stock market.' },
      { icon: 'mdi-account-group', title: 'Compete with Friends', description: 'Create leagues, invite friends, and see who can build the best performing portfolio.' },
      { icon: 'mdi-chart-timeline-variant', title: 'Real World Prices', description: 'Make plays based on real world prices. We operate on a slight delay so you can catch big moves in the market live and get your bet in on Moq Exchange.' },
    ],
  }),
  computed: {
    ...mapGetters('auth', ['isAuthenticated']),
  },
  mounted() {
    // Trigger feature card animations when they scroll into view
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            this.featuresVisible = true;
            observer.disconnect();
          }
        });
      },
      { threshold: 0.2 }
    );
    if (this.$refs.featuresTitle) {
      observer.observe(this.$refs.featuresTitle);
    }
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
.landing-page {
  overflow-x: hidden;
}

/* ── Hero ── */
.hero-section {
  position: relative;
  background: linear-gradient(135deg, #2e7d32, #1976D2);
  color: white;
  padding: 0 24px;
  padding-bottom: 80px;
  overflow: hidden;
}

.hero-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  min-height: 85vh;
  position: relative;
  z-index: 1;
  padding: 60px 0 0;
  max-width: 640px;
  margin: 0 auto;
}

/* ── Bubbles ── */
.bubbles {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}

.bubble {
  position: absolute;
  bottom: -60px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.06);
  animation: float-up linear infinite;
}

.bubble:nth-child(1)  { width: 40px;  height: 40px;  left: 6%;   animation-duration: 11s; animation-delay: 0s; }
.bubble:nth-child(2)  { width: 24px;  height: 24px;  left: 15%;  animation-duration: 9s;  animation-delay: 1s; }
.bubble:nth-child(3)  { width: 56px;  height: 56px;  left: 25%;  animation-duration: 14s; animation-delay: 2.5s; }
.bubble:nth-child(4)  { width: 32px;  height: 32px;  left: 35%;  animation-duration: 10s; animation-delay: 0.5s; }
.bubble:nth-child(5)  { width: 20px;  height: 20px;  left: 45%;  animation-duration: 8s;  animation-delay: 3s; }
.bubble:nth-child(6)  { width: 48px;  height: 48px;  left: 55%;  animation-duration: 13s; animation-delay: 1.5s; }
.bubble:nth-child(7)  { width: 28px;  height: 28px;  left: 65%;  animation-duration: 10s; animation-delay: 4s; }
.bubble:nth-child(8)  { width: 60px;  height: 60px;  left: 75%;  animation-duration: 15s; animation-delay: 0s; }
.bubble:nth-child(9)  { width: 18px;  height: 18px;  left: 82%;  animation-duration: 9s;  animation-delay: 2s; }
.bubble:nth-child(10) { width: 36px;  height: 36px;  left: 90%;  animation-duration: 12s; animation-delay: 3.5s; }
.bubble:nth-child(11) { width: 22px;  height: 22px;  left: 10%;  animation-duration: 11s; animation-delay: 5s; }
.bubble:nth-child(12) { width: 44px;  height: 44px;  left: 50%;  animation-duration: 16s; animation-delay: 1s; }

@keyframes float-up {
  0% {
    transform: translateY(0) scale(1);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    transform: translateY(-110vh) scale(1.15);
    opacity: 0;
  }
}

.hero-tagline {
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 2px;
  color: rgba(255, 255, 255, 0.7);
}

.hero-title {
  font-size: clamp(2rem, 5vw, 3.2rem);
  font-weight: 800;
  line-height: 1.15;
  letter-spacing: -0.5px;
}

.hero-subtitle {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.75);
  line-height: 1.6;
  max-width: 520px;
  margin-left: auto;
  margin-right: auto;
}

.hero-cta-primary {
  color: #2e7d32 !important;
  font-weight: 700;
}

.hero-cta-secondary {
  color: white !important;
  border-color: rgba(255, 255, 255, 0.4) !important;
}

/* Scroll indicator */
.scroll-indicator {
  text-align: center;
  padding-bottom: 40px;
}

.bounce-arrow {
  animation: bounce 2s ease infinite;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(8px); }
  60% { transform: translateY(4px); }
}

/* Wave SVG at bottom of hero */
.hero-wave {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  line-height: 0;
}

.hero-wave svg {
  width: 100%;
  height: 80px;
}

/* ── Features ── */
.features-section {
  background: #fff;
  position: relative;
  z-index: 1;
  padding: 64px 24px;
}

.features-inner {
  max-width: 1100px;
  margin: 0 auto;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
}

.section-divider {
  width: 50px;
  height: 3px;
  background: linear-gradient(to right, #4CAF50, #2196F3);
  margin: 10px auto 0;
  border-radius: 2px;
}

.feature-card {
  border-radius: 12px;
  transition: transform 0.25s ease, box-shadow 0.25s ease;
  opacity: 0;
  transform: translateY(30px);
}

.feature-card.anim-visible {
  animation: slide-up-fade 0.6s ease forwards;
}

.feature-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.1) !important;
}

.feature-icon-bg {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
  border-radius: 16px;
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.1), rgba(33, 150, 243, 0.1));
}

/* ── CTA ── */
.cta-section {
  position: relative;
  background: linear-gradient(135deg, #1976D2, #2e7d32);
}

.cta-wave-top {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  line-height: 0;
}

.cta-wave-top svg {
  width: 100%;
  height: 60px;
}

.cta-inner {
  text-align: center;
  padding: 80px 24px 64px;
  max-width: 640px;
  margin: 0 auto;
}

.cta-btn {
  color: #1976D2 !important;
  font-weight: 700;
}

/* ── Footer ── */
.landing-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 24px;
  border-top: 1px solid rgba(0, 0, 0, 0.08);
}

/* ── Animations ── */
.anim-fade-down {
  animation: fade-down 0.7s ease both;
}

.anim-fade-up {
  animation: fade-up 0.7s ease both;
}

.anim-delay-1 { animation-delay: 0.15s; }
.anim-delay-2 { animation-delay: 0.3s; }
.anim-delay-3 { animation-delay: 0.5s; }

@keyframes fade-down {
  from { opacity: 0; transform: translateY(-20px); }
  to   { opacity: 1; transform: translateY(0); }
}

@keyframes fade-up {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}

@keyframes slide-up-fade {
  from { opacity: 0; transform: translateY(30px); }
  to   { opacity: 1; transform: translateY(0); }
}
</style>
