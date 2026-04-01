<template>
    <v-container fluid class="faq-container pa-0">
      <v-row align="center" justify="center" class="mx-0">
        <v-col cols="12" md="10" lg="8">
          <v-card elevation="12" class="pa-6 main-card">
            <v-card-title class="text-h4 font-weight-bold text-center mb-4 white--text">
              How to Play
            </v-card-title>
            
            <v-expansion-panels>
              <v-expansion-panel
                v-for="(item, i) in faqItems"
                :key="i"
              >
                <v-expansion-panel-header class="title panel-header">
                  {{ item.question }}
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                  <v-card-text class="panel-content" v-html="item.answer"></v-card-text>
                </v-expansion-panel-content>
              </v-expansion-panel>
            </v-expansion-panels>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
</template>

<script>
export default {
  name: 'FAQPage',
  data() {
    return {
      faqItems: [
        {
          question: 'What is the Weekly Draft?',
          answer: `
            <p>The weekly draft is your chance to play the market with a new strategy each week. Build gains to buy packs from the Bazaar or increase your shares in stocks from your persistent portfolio:</p>
            <ul>
              <li>You're given a 50k stake to wrangle up a selection of stocks for the week.</li>
              <li>The stock corral changes weekly, offering different industries or select symbols.</li>
              <li>Your gains can be used to buy packs in the Bazaar or to increase your shares in stocks from packs or the player market.</li>
              <li>Remember, you can't earn Moq (our persistent currency) through the weekly draft.</li>
            </ul>
          `
        },
        {
          question: 'How does the Bazaar work?',
          answer: `
            <p>The Bazaar is where the real trading happens, trade with other players and grow your persistent portfolio:</p>
            <ul>
              <li>Use your weekly gains to buy packs of 5 random stocks from a surprise industry.</li>
              <li>From your inventory, you can "lock in" stocks for your persistent portfolio or "list" them on the player market.</li>
              <li>Set your own prices in Moq for listed stocks, just like at a frontier auction.</li>
              <li>Locked-in stocks join your persistent portfolio. Buy more shares with gains or sell for Moq.</li>
              <li>Keep an eye on your inventory limits - you can expand them by spending Moq.</li>
            </ul>
          `
        },
        {
          question: 'What is the Persistent Portfolio and how do Tags work?',
          answer: `
            <p>The Persistent Portfolio is your long-term investment strategy that doesn't reset weekly:</p>
            <ul>
              <li>Unlike the weekly portfolio, stocks in your persistent portfolio carry over week to week, only being reset at the start of a new season.</li>
              <li>You can add stocks to your persistent portfolio by "locking in" stocks from your inventory.</li>
              <li>Stocks in your persistent portfolio can have special Tags that give them unique properties.</li>
            </ul>
            <p>Tags add an extra layer of strategy to your trades. Here's how each tag works:</p>
            <ul>
              <li><strong>COMMISSION (Sell Value Multiplier):</strong> When you sell a stock with this tag, you have a % chance to receive a bonus multiplier on the sell value.</li>
              <li><strong>TENACIOUS (Chance to Keep Shares):</strong> There's a % chance you'll keep some shares when selling a stock with this tag.</li>
              <li><strong>SUBSIDIZED (Bonus Sell Value):</strong> Selling a stock with this tag will give you a flat bonus on top of the regular sell value.</li>
              <li><strong>INSIDER (Chance to Buy Bonus Shares):</strong> When buying a stock with this tag, you have a % chance to receive bonus shares at no extra cost.</li>
              <li><strong>GLITCHED (Chance to Change into Random Stock):</strong> Stocks with this tag have a 10%chance to transform into a different random stock from the same industry when bought or sold.</li>
            </ul>
            <p>Remember, these tags can significantly impact your trading strategy. Use them wisely to maximize your gains in the long run!</p>
          `
        },
        {
          question: 'What are the Leaderboards about?',
          answer: `
            <p>Our leaderboards show who's the top dog in the trading world:</p>
            <ul>
              <li>Weekly leaderboard showcases the highest portfolio gains in the weekly challenge.</li>
              <li>The Moq leaderboard displays players with the highest total Moqs.</li>
              <li>Total Moqs are calculated as (persistent portfolio value + total Moqs).</li>
            </ul>
          `
        },
      ]
    }
  }
}
</script>

<style scoped>
.faq-container {
  background: linear-gradient(to right, #4CAF50, #2196F3);
  min-height: 100vh;
  padding: 2rem 0;
}

.main-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 2rem; /* Added padding to the main card */
}

.v-card-title {
  text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
  margin-bottom: 1.5rem; /* Increased bottom margin */
}

.v-expansion-panels {
  background: transparent;
}

.v-expansion-panel {
  background: rgba(255, 255, 255, 0.15);
  margin-bottom: 1rem;
  border-radius: 15px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.v-expansion-panel:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.2);
}

.panel-header {
  background: linear-gradient(45deg, #3949AB, #1E88E5);
  color: #FFFFFF;
  font-weight: bold;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
  padding: 1rem 1.5rem; /* Increased padding */
}

.panel-content {
  background: linear-gradient(to right, #E8F5E9, #E3F2FD);
  color: #1E1E1E;
  border-top: 2px solid #BBDEFB;
  padding: 1.5rem; /* Increased padding */
}

.panel-content p {
  margin-bottom: 1rem; /* Increased bottom margin */
}

.panel-content ul {
  padding-left: 2rem; /* Increased left padding */
  list-style-type: none;
}

.panel-content li {
  margin-bottom: 1rem; /* Increased bottom margin */
  position: relative;
  padding-left: 1.5rem; /* Added left padding to list items */
}

.panel-content li:before {
  content: '🌟';
  position: absolute;
  left: -5px; /* Adjusted position */
  top: 0;
}

/* Added styles for better text wrapping */
.v-expansion-panel-content__wrap {
  white-space: normal;
  word-wrap: break-word;
  overflow-wrap: break-word;
}
</style>
